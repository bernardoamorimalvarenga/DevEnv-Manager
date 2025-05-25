#!/usr/bin/env python3
"""
EnvForge - Main CLI Interface
"""
from datetime import datetime

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from ..core.detector import detector
from ..core.restorer import restorer
from ..core.sync import git_sync
from ..storage.local import storage

console = Console()


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """EnvForge - Forge, sync and restore complete development environments in minutes!"""


@cli.command()
def init():
    """Initialize EnvForge in current directory"""
    console.print(
        Panel.fit(
            "[bold green]🔥 EnvForge initialized "
            "successfully![/bold green]\n"
            f"Config stored in: {storage.snapshots_dir.parent}",
            title="Init Complete",
        )
    )


@cli.command()
@click.argument("name")
def capture(name):
    """Capture current development environment"""
    console.print(
        f"[bold blue]🔥 Capturing environment: {name}[/bold blue]"
    )

    with console.status("[bold green]Detecting system configuration..."):
        # Collect system data
        data = {
            "system_info": detector.get_system_info(),
            "packages": detector.detect_packages(),
            "dotfiles": detector.detect_dotfiles(),
            "vscode_extensions": detector.detect_vscode_extensions(),
        }

    # Save snapshot
    if storage.save_snapshot(name, data):
        # Show summary
        table = Table(title="Capture Summary")
        table.add_column("Component", style="cyan")
        table.add_column("Count", style="green")

        table.add_row("APT Packages", str(len(data["packages"]["apt"])))
        table.add_row("Snap Packages", str(len(data["packages"]["snap"])))
        table.add_row(
            "Flatpak Packages", str(len(data["packages"]["flatpak"]))
        )
        table.add_row("PIP Packages", str(len(data["packages"]["pip"])))
        table.add_row("Dotfiles", str(len(data["dotfiles"])))
        table.add_row(
            "VS Code Extensions", str(len(data["vscode_extensions"]))
        )

        console.print(table)
        console.print(
            f"[green]✓ Environment '{name}' captured "
            "successfully![/green]"
        )
    else:
        console.print("[red]✗ Failed to capture environment![/red]")


@cli.command()
def list():
    """List all captured environments"""
    snapshots = storage.list_snapshots()

    if not snapshots:
        console.print(
            "[yellow]📋 No environments found. Use 'envforge capture "
            "<name>' to create one.[/yellow]"
        )
        return

    table = Table(title="Available Environments")
    table.add_column("Name", style="cyan")
    table.add_column("Created", style="green")
    table.add_column("File", style="dim")

    for snapshot in snapshots:
        created_date = datetime.fromisoformat(
            snapshot["created_at"]
        ).strftime("%Y-%m-%d %H:%M")
        table.add_row(snapshot["name"], created_date, snapshot["file"])

    console.print(table)


@cli.command()
@click.argument("name")
def show(name):
    """Show details of a captured environment"""
    data = storage.load_snapshot(name)

    if not data:
        console.print(f"[red]❌ Environment '{name}' not found![/red]")
        return

    console.print(f"[bold cyan]📋 Environment Details: {name}[/bold cyan]")

    # System info
    if "system_info" in data:
        info_table = Table(title="System Information")
        info_table.add_column("Property", style="cyan")
        info_table.add_column("Value", style="green")

        for key, value in data["system_info"].items():
            info_table.add_row(key.replace("_", " ").title(), str(value))

        console.print(info_table)

    # Packages summary
    if "packages" in data:
        pkg_table = Table(title="Packages Summary")
        pkg_table.add_column("Type", style="cyan")
        pkg_table.add_column("Count", style="green")

        for pkg_type, packages in data["packages"].items():
            if packages:
                pkg_table.add_row(pkg_type.upper(), str(len(packages)))

        console.print(pkg_table)


@cli.command()
@click.argument("name")
@click.option(
    "--dry-run",
    is_flag=True,
    help="Show what would be done without making changes",
)
@click.option("--force", is_flag=True, help="Skip confirmation prompts")
def restore(name, dry_run, force):
    """Restore a captured environment"""
    # Load snapshot data
    data = storage.load_snapshot(name)

    if not data:
        console.print(f"[red]❌ Environment '{name}' not found![/red]")
        return

    console.print(
        f"[bold magenta]🔄 Restoring environment: "
        f"{name}[/bold magenta]"
    )

    # Show what will be restored
    if "packages" in data:
        pkg_table = Table(title="Packages to Restore")
        pkg_table.add_column("Type", style="cyan")
        pkg_table.add_column("Count", style="green")

        total_packages = 0
        for pkg_type, packages in data["packages"].items():
            if packages:
                pkg_table.add_row(pkg_type.upper(), str(len(packages)))
                total_packages += len(packages)

        console.print(pkg_table)

        if not dry_run and not force:
            console.print(
                f"\n[yellow]⚠️  This will install "
                f"{total_packages} packages and may modify your "
                "system.[/yellow]"
            )
            if not click.confirm("Do you want to continue?"):
                console.print("[yellow]Restore cancelled.[/yellow]")
                return

    # Perform restoration
    success = restorer.restore_environment(data, dry_run=dry_run)

    if success:
        if dry_run:
            console.print(
                "[green]✓ Dry run completed successfully![/green]"
            )
        else:
            console.print(
                "[green]✓ Environment restored " "successfully![/green]"
            )
    else:
        console.print(
            "[red]✗ Some errors occurred during " "restoration![/red]"
        )


@cli.command()
def status():
    """Show current system status and available packages"""
    console.print("[bold cyan]📊 System Status[/bold cyan]")

    with console.status("[bold green]Analyzing system..."):
        system_info = detector.get_system_info()
        packages = detector.detect_packages()

    # System info table
    info_table = Table(title="System Information")
    info_table.add_column("Property", style="cyan")
    info_table.add_column("Value", style="green")

    for key, value in system_info.items():
        info_table.add_row(key.replace("_", " ").title(), str(value))

    console.print(info_table)

    # Packages summary
    pkg_table = Table(title="Installed Packages")
    pkg_table.add_column("Type", style="cyan")
    pkg_table.add_column("Count", style="green")

    for pkg_type, pkg_list in packages.items():
        if pkg_list:
            pkg_table.add_row(pkg_type.upper(), str(len(pkg_list)))

    console.print(pkg_table)


@cli.command()
@click.argument("name")
@click.option("--force", is_flag=True, help="Skip confirmation prompt")
def delete(name, force):
    """Delete a captured environment"""
    # Check if environment exists
    data = storage.load_snapshot(name)
    if not data:
        console.print(f"[red]❌ Environment '{name}' not found![/red]")
        return

    # Confirmation
    if not force:
        console.print(
            f"[yellow]⚠️  This will permanently delete "
            f"environment '{name}'[/yellow]"
        )
        if not click.confirm("Are you sure?"):
            console.print("[yellow]Delete cancelled.[/yellow]")
            return

    # Delete the environment
    if storage.delete_snapshot(name):
        console.print(
            f"[green]✓ Environment '{name}' deleted "
            "successfully![/green]"
        )
    else:
        console.print(
            f"[red]✗ Failed to delete environment " f"'{name}'![/red]"
        )


@cli.command()
@click.argument("name")
@click.argument("output_file", type=click.Path())
def export(name, output_file):
    """Export an environment to a file"""
    data = storage.load_snapshot(name)

    if not data:
        console.print(f"[red]❌ Environment '{name}' not found![/red]")
        return

    try:
        import json

        with open(output_file, "w") as f:
            json.dump(data, f, indent=2)

        console.print(
            f"[green]✓ Environment '{name}' exported to "
            f"{output_file}![/green]"
        )
    except Exception as e:
        console.print(f"[red]✗ Failed to export environment: {e}[/red]")


@cli.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.option(
    "--name",
    help="Name for the imported environment "
    "(defaults to original name)",
)
def import_env(input_file, name):
    """Import an environment from a file"""
    try:
        import json

        with open(input_file, "r") as f:
            data = json.load(f)

        # Use provided name or original name
        env_name = name or data.get("metadata", {}).get(
            "name", "imported-env"
        )

        # Check if already exists
        if storage.load_snapshot(env_name):
            console.print(
                f"[yellow]⚠️  Environment '{env_name}' already "
                "exists![/yellow]"
            )
            if not click.confirm("Overwrite existing environment?"):
                console.print("[yellow]Import cancelled.[/yellow]")
                return

        # Save imported environment
        if storage.save_snapshot(env_name, data):
            console.print(
                f"[green]✓ Environment imported as "
                f"'{env_name}'![/green]"
            )
        else:
            console.print("[red]✗ Failed to import environment![/red]")

    except Exception as e:
        console.print(f"[red]✗ Failed to import environment: {e}[/red]")


@cli.command()
@click.argument("env1")
@click.argument("env2")
def diff(env1, env2):
    """Compare two environments and show differences"""
    # Load both environments
    data1 = storage.load_snapshot(env1)
    data2 = storage.load_snapshot(env2)

    if not data1:
        console.print(f"[red]❌ Environment '{env1}' not found![/red]")
        return

    if not data2:
        console.print(f"[red]❌ Environment '{env2}' not found![/red]")
        return

    console.print(f"[bold cyan]🔍 Comparing {env1} vs {env2}[/bold cyan]")

    # Compare packages
    if "packages" in data1 and "packages" in data2:
        _compare_packages(data1["packages"], data2["packages"], env1, env2)

    # Compare dotfiles
    if "dotfiles" in data1 and "dotfiles" in data2:
        _compare_dotfiles(data1["dotfiles"], data2["dotfiles"], env1, env2)

    # Compare VS Code extensions
    if "vscode_extensions" in data1 and "vscode_extensions" in data2:
        _compare_extensions(
            data1["vscode_extensions"],
            data2["vscode_extensions"],
            env1,
            env2,
        )


def _compare_packages(pkg1, pkg2, name1, name2):
    """Compare package lists between two environments"""
    console.print("\n[bold]📦 Package Differences:[/bold]")

    for pkg_type in ["apt", "snap", "flatpak", "pip"]:
        set1 = set(pkg1.get(pkg_type, []))
        set2 = set(pkg2.get(pkg_type, []))

        only_in_1 = set1 - set2
        only_in_2 = set2 - set1

        if only_in_1 or only_in_2:
            console.print(f"\n[cyan]{pkg_type.upper()} packages:[/cyan]")

            if only_in_1:
                console.print(
                    f"  Only in {name1}: {len(only_in_1)} " "packages"
                )
                for pkg in sorted(list(only_in_1)[:5]):  # Show first 5
                    console.print(f"    - {pkg}")
                if len(only_in_1) > 5:
                    console.print(f"    ... and {len(only_in_1) - 5} more")

            if only_in_2:
                console.print(
                    f"  Only in {name2}: {len(only_in_2)} " "packages"
                )
                for pkg in sorted(list(only_in_2)[:5]):  # Show first 5
                    console.print(f"    + {pkg}")
                if len(only_in_2) > 5:
                    console.print(f"    ... and {len(only_in_2) - 5} more")


def _compare_dotfiles(dotfiles1, dotfiles2, name1, name2):
    """Compare dotfiles between two environments"""
    console.print("\n[bold]📝 Dotfile Differences:[/bold]")

    set1 = set(dotfiles1.keys())
    set2 = set(dotfiles2.keys())

    only_in_1 = set1 - set2
    only_in_2 = set2 - set1
    common = set1 & set2

    if only_in_1:
        console.print(f"  Only in {name1}: {', '.join(sorted(only_in_1))}")

    if only_in_2:
        console.print(f"  Only in {name2}: {', '.join(sorted(only_in_2))}")

    # Check for content differences in common files
    different_content = []
    for filename in common:
        if dotfiles1[filename] != dotfiles2[filename]:
            different_content.append(filename)

    if different_content:
        console.print(
            f"  Different content: "
            f"{', '.join(sorted(different_content))}"
        )


def _compare_extensions(ext1, ext2, name1, name2):
    """Compare VS Code extensions between two environments"""
    console.print("\n[bold]🔌 VS Code Extension Differences:[/bold]")

    set1 = set(ext1)
    set2 = set(ext2)

    only_in_1 = set1 - set2
    only_in_2 = set2 - set1

    if only_in_1:
        console.print(f"  Only in {name1}: {len(only_in_1)} extensions")
        for ext in sorted(list(only_in_1)[:3]):
            console.print(f"    - {ext}")
        if len(only_in_1) > 3:
            console.print(f"    ... and {len(only_in_1) - 3} more")

    if only_in_2:
        console.print(f"  Only in {name2}: {len(only_in_2)} extensions")
        for ext in sorted(list(only_in_2)[:3]):
            console.print(f"    + {ext}")
        if len(only_in_2) > 3:
            console.print(f"    ... and {len(only_in_2) - 3} more")


@cli.command()
def clean():
    """Clean up old backup files and temporary data"""
    cleaned_files = 0

    # Clean up dotfile backups older than 30 days
    import time
    from pathlib import Path

    home_dir = Path.home()
    current_time = time.time()

    for backup_file in home_dir.glob("*/.envforge-backup"):
        try:
            file_age = current_time - backup_file.stat().st_mtime
            if file_age > (30 * 24 * 3600):  # 30 days
                backup_file.unlink()
                cleaned_files += 1
        except Exception:
            pass

    console.print(
        f"[green]✓ Cleaned up {cleaned_files} old backup " "files[/green]"
    )


# =====================
# SYNC COMMANDS
# =====================


@cli.group()
def sync():
    """Git-based synchronization commands"""


@sync.command()
@click.argument("repo_url")
@click.option("--branch", default="main", help="Git branch to use")
def setup(repo_url, branch):
    """Setup git sync with a remote repository"""
    console.print(f"[blue]🔧 Setting up git sync with {repo_url}[/blue]")

    if git_sync.setup_sync(repo_url, branch):
        console.print(
            Panel.fit(
                f"[bold green]Git sync setup complete![/bold green]\n\n"
                f"Repository: {repo_url}\n"
                f"Branch: {branch}\n\n"
                f"Use 'envforge sync push' to upload environments\n"
                f"Use 'envforge sync pull' to download environments",
                title="Sync Ready",
            )
        )
    else:
        console.print("[red]✗ Failed to setup git sync[/red]")


@sync.command()
@click.option(
    "--env", "-e", multiple=True, help="Specific environments to push"
)
def push(env):
    """Push environments to remote repository

    Examples:
      envforge sync push                    # Push all environments
      envforge sync push -e myenv          # Push specific environment
      envforge sync push -e env1 -e env2   # Push multiple environments
    """
    # Construir lista de ambientes (evitar list() direto por bug do Click)
    if env and len(env) > 0:
        env_list = []
        for item in env:
            env_list.append(item)
        console.print(
            f"[blue]📤 Pushing specific environments: "
            f"{', '.join(env_list)}[/blue]"
        )
    else:
        env_list = None
        console.print("[blue]📤 Pushing all environments...[/blue]")

    # Executar push
    result = git_sync.push_environments(env_list)

    # Mostrar resultado
    if result:
        if env_list:
            console.print(
                f"[green]✓ Successfully pushed "
                f"{len(env_list)} specific "
                "environments[/green]"
            )
        else:
            console.print(
                "[green]✓ Successfully pushed all " "environments[/green]"
            )
    else:
        console.print("[red]✗ Push operation failed[/red]")


@sync.command()
def pull():
    """Pull environments from remote repository"""
    git_sync.pull_environments()


@sync.command()
def sync_status():
    """Show git sync status"""
    status_info = git_sync.sync_status()

    if not status_info.get("enabled"):
        console.print("[yellow]📡 Git sync not configured[/yellow]")
        console.print("Run 'envforge sync setup <repo-url>' to get started")
        return

    # Create status table
    table = Table(title="Git Sync Status")
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="green")

    table.add_row(
        "Status", "✓ Enabled" if status_info["enabled"] else "✗ Disabled"
    )

    if "remote_url" in status_info:
        table.add_row("Remote URL", status_info["remote_url"])

    if "branch" in status_info:
        table.add_row("Branch", status_info["branch"])

    if "uncommitted_changes" in status_info:
        changes_status = (
            "Yes" if status_info["uncommitted_changes"] else "No"
        )
        table.add_row("Uncommitted Changes", changes_status)

    if "last_commit" in status_info and status_info["last_commit"]:
        commit = status_info["last_commit"]
        table.add_row(
            "Last Commit", f"{commit['hash']} - {commit['message']}"
        )
        table.add_row("Commit Date", commit["date"])

    if "sync_dir" in status_info:
        table.add_row("Sync Directory", status_info["sync_dir"])

    console.print(table)

    if status_info.get("error"):
        console.print(f"[red]Error: {status_info['error']}[/red]")


if __name__ == "__main__":
    cli()