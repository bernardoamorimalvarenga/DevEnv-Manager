"""
Git-based synchronization for EnvForge
"""

import json
import subprocess
from typing import Any, Dict, List, Optional

import click
from rich.console import Console

from ..core.config import config
from ..storage.local import storage

console = Console()


class GitSync:
    def __init__(self):
        self.sync_dir = config.config_dir / "sync"
        self.repo = None
        self.remote_url = None

    def setup_sync(self, remote_url: str, branch: str = "main") -> bool:
        """Setup git sync with a remote repository"""
        try:
            # Create sync directory
            self.sync_dir.mkdir(exist_ok=True)

            # Initialize git repo if needed
            if not (self.sync_dir / ".git").exists():
                subprocess.run(
                    ["git", "init"],
                    cwd=self.sync_dir,
                    check=True,
                    capture_output=True,
                )

                # Create initial commit
                readme_content = """# EnvForge Sync Repository

This repository contains synchronized development environments.
Generated automatically by EnvForge.

## Contents
- `environments/` - Environment snapshots
- `metadata.json` - Sync metadata

Do not edit these files manually.
"""
                with open(self.sync_dir / "README.md", "w") as f:
                    f.write(readme_content)

                # Create environments directory
                (self.sync_dir / "environments").mkdir(exist_ok=True)

                # Create metadata file
                metadata = {
                    "version": "0.1.0",
                    "created_by": "envforge",
                    "last_sync": None,
                    "environments": {},
                }
                with open(self.sync_dir / "metadata.json", "w") as f:
                    json.dump(metadata, f, indent=2)

                # Initial commit
                subprocess.run(
                    ["git", "add", "."],
                    cwd=self.sync_dir,
                    check=True,
                    capture_output=True,
                )
                subprocess.run(
                    [
                        "git",
                        "commit",
                        "-m",
                        "Initial EnvForge sync setup",
                    ],
                    cwd=self.sync_dir,
                    check=True,
                    capture_output=True,
                )

            # Add remote if not exists
            try:
                subprocess.run(
                    ["git", "remote", "add", "origin", remote_url],
                    cwd=self.sync_dir,
                    check=True,
                    capture_output=True,
                )
            except subprocess.CalledProcessError:
                # Remote might already exist, try to set URL
                subprocess.run(
                    ["git", "remote", "set-url", "origin", remote_url],
                    cwd=self.sync_dir,
                    check=True,
                    capture_output=True,
                )

            # Set branch
            subprocess.run(
                ["git", "branch", "-M", branch],
                cwd=self.sync_dir,
                check=True,
                capture_output=True,
            )

            self.remote_url = remote_url

            # Save sync config
            config.settings["sync"] = {
                "enabled": True,
                "remote_url": remote_url,
                "branch": branch,
                "last_sync": None,
            }
            config.save_config()

            console.print(
                f"[green]✓ Git sync setup successfully with "
                f"{remote_url}[/green]"
            )
            return True

        except subprocess.CalledProcessError as e:
            console.print(f"[red]✗ Git sync setup failed: {e}[/red]")
            return False
        except Exception as e:
            console.print(f"[red]✗ Sync setup error: {e}[/red]")
            return False

    def push_environments(
        self, environment_names: Optional[List[str]] = None
    ) -> bool:
        """Push environments to remote repository"""
        if not self._check_sync_setup():
            return False

        try:
            # Get environments to sync
            if environment_names is None:
                snapshots = storage.list_snapshots()
                environment_names = [s["name"] for s in snapshots]

            if not environment_names:
                console.print("[yellow]No environments to sync[/yellow]")
                return True

            console.print(
                f"[blue]📤 Pushing {len(environment_names)} "
                "environments...[/blue]"
            )

            # Copy environments to sync directory
            env_dir = self.sync_dir / "environments"
            env_dir.mkdir(exist_ok=True)

            synced_count = 0
            for env_name in environment_names:
                data = storage.load_snapshot(env_name)
                if data:
                    env_file = env_dir / f"{env_name}.json"
                    with open(env_file, "w") as f:
                        json.dump(data, f, indent=2)
                    synced_count += 1

            # Update metadata
            self._update_metadata(environment_names)

            # Git operations
            subprocess.run(
                ["git", "add", "."],
                cwd=self.sync_dir,
                check=True,
                capture_output=True,
            )

            # Check if there are changes to commit
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=self.sync_dir,
                capture_output=True,
                text=True,
            )

            if result.stdout.strip():
                # Commit changes
                commit_msg = f"Sync {synced_count} environments"
                subprocess.run(
                    ["git", "commit", "-m", commit_msg],
                    cwd=self.sync_dir,
                    check=True,
                    capture_output=True,
                )

                # Push to remote
                subprocess.run(
                    ["git", "push", "-u", "origin", "main"],
                    cwd=self.sync_dir,
                    check=True,
                    capture_output=True,
                )

                console.print(
                    f"[green]✓ Successfully pushed "
                    f"{synced_count} environments[/green]"
                )
            else:
                console.print("[yellow]No changes to sync[/yellow]")

            return True

        except subprocess.CalledProcessError as e:
            console.print(f"[red]✗ Push failed: {e}[/red]")
            return False
        except Exception as e:
            console.print(f"[red]✗ Push error: {e}[/red]")
            return False

    def pull_environments(self) -> bool:
        """Pull environments from remote repository"""
        if not self._check_sync_setup():
            return False

        try:
            console.print(
                "[blue]📥 Pulling environments from " "remote...[/blue]"
            )

            # Pull from remote
            subprocess.run(
                ["git", "pull", "origin", "main"],
                cwd=self.sync_dir,
                check=True,
                capture_output=True,
            )

            # Import environments from sync directory
            env_dir = self.sync_dir / "environments"
            if not env_dir.exists():
                console.print(
                    "[yellow]No environments found in remote "
                    "repository[/yellow]"
                )
                return True

            return self._import_environments_from_sync_dir(env_dir)

        except subprocess.CalledProcessError as e:
            console.print(f"[red]✗ Pull failed: {e}[/red]")
            return False
        except Exception as e:
            console.print(f"[red]✗ Pull error: {e}[/red]")
            return False

    def _import_environments_from_sync_dir(self, env_dir) -> bool:
        """Import environments from sync directory"""
        imported_count = 0

        for env_file in env_dir.glob("*.json"):
            try:
                with open(env_file, "r") as f:
                    data = json.load(f)

                env_name = env_file.stem

                # Check if environment already exists locally
                existing_data = storage.load_snapshot(env_name)
                if existing_data:
                    if not self._should_overwrite_local_env(
                        env_name, data, existing_data
                    ):
                        continue

                # Import environment
                if storage.save_snapshot(env_name, data):
                    imported_count += 1
                    console.print(f"[green]✓ Imported {env_name}[/green]")

            except Exception as e:
                console.print(
                    f"[red]✗ Failed to import " f"{env_file.name}: {e}[/red]"
                )

        console.print(
            f"[green]✓ Successfully imported "
            f"{imported_count} environments[/green]"
        )
        return True

    def _should_overwrite_local_env(
        self, env_name, remote_data, local_data
    ) -> bool:
        """Check if local environment should be overwritten"""
        # Compare timestamps or ask user
        remote_time = remote_data.get("metadata", {}).get("created_at", "")
        local_time = local_data.get("metadata", {}).get("created_at", "")

        if remote_time <= local_time:
            console.print(
                f"[dim]Skipping {env_name} (local version is " "newer)[/dim]"
            )
            return False

        console.print(
            f"[yellow]Environment '{env_name}' already exists "
            "locally[/yellow]"
        )
        return click.confirm(f"Overwrite local version of '{env_name}'?")

    def sync_status(self) -> Dict[str, Any]:
        """Get sync status information"""
        if not self._check_sync_setup():
            return {"enabled": False}

        try:
            # Get git status
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=self.sync_dir,
                capture_output=True,
                text=True,
            )

            uncommitted_changes = bool(result.stdout.strip())

            # Get last commit info
            try:
                result = subprocess.run(
                    ["git", "log", "-1", "--format=%H|%s|%ai"],
                    cwd=self.sync_dir,
                    capture_output=True,
                    text=True,
                    check=True,
                )
                last_commit_info = result.stdout.strip().split("|")
                last_commit = {
                    "hash": last_commit_info[0][:8],
                    "message": last_commit_info[1],
                    "date": last_commit_info[2],
                }
            except Exception:
                last_commit = None

            return {
                "enabled": True,
                "remote_url": (
                    self.remote_url or config.get("sync.remote_url")
                ),
                "branch": "main",
                "uncommitted_changes": uncommitted_changes,
                "last_commit": last_commit,
                "sync_dir": str(self.sync_dir),
            }

        except Exception as e:
            return {"enabled": True, "error": str(e)}

    def _check_sync_setup(self) -> bool:
        """Check if sync is properly setup"""
        if not config.get("sync.enabled"):
            console.print(
                "[red]✗ Git sync not setup. Run 'envforge sync "
                "setup <repo-url>' first[/red]"
            )
            return False

        if not self.sync_dir.exists() or not (self.sync_dir / ".git").exists():
            console.print(
                "[red]✗ Git sync directory corrupted. Run setup " "again[/red]"
            )
            return False

        return True

    def _update_metadata(self, environment_names: List[str]):
        """Update sync metadata"""
        from datetime import datetime

        metadata_file = self.sync_dir / "metadata.json"

        if metadata_file.exists():
            with open(metadata_file, "r") as f:
                metadata = json.load(f)
        else:
            metadata = {"environments": {}}

        metadata["last_sync"] = datetime.now().isoformat()

        for env_name in environment_names:
            metadata["environments"][env_name] = {
                "last_synced": datetime.now().isoformat()
            }

        with open(metadata_file, "w") as f:
            json.dump(metadata, f, indent=2)


# Global sync instance
git_sync = GitSync()