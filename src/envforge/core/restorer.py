"""
Environment restoration utilities for EnvForge
"""

import subprocess
from pathlib import Path
from typing import Any, Dict, List

from rich.console import Console

console = Console()


class EnvironmentRestorer:
    def __init__(self):
        self.home_dir = Path.home()
        self.dry_run = False

    def restore_environment(
        self, data: Dict[str, Any], dry_run: bool = False
    ) -> bool:
        """Restore a complete environment from snapshot data"""
        self.dry_run = dry_run

        if dry_run:
            console.print(
                "[yellow]🔍 DRY RUN MODE - No changes will be " "made[/yellow]"
            )

        success = True

        # Restore packages
        if "packages" in data:
            success &= self._restore_packages(data["packages"])

        # Restore dotfiles
        if "dotfiles" in data:
            success &= self._restore_dotfiles(data["dotfiles"])

        # Restore VS Code extensions
        if "vscode_extensions" in data:
            success &= self._restore_vscode_extensions(
                data["vscode_extensions"]
            )

        return success

    def _restore_packages(self, packages: Dict[str, List[str]]) -> bool:
        """Restore system packages"""
        console.print("[bold blue]📦 Restoring packages...[/bold blue]")

        success = True

        # APT packages
        if packages.get("apt"):
            console.print(
                f"Installing {len(packages['apt'])} APT " "packages..."
            )
            success &= self._install_apt_packages(packages["apt"])

        # Snap packages
        if packages.get("snap"):
            console.print(
                f"Installing {len(packages['snap'])} Snap " "packages..."
            )
            success &= self._install_snap_packages(packages["snap"])

        # Flatpak packages
        if packages.get("flatpak"):
            console.print(
                f"Installing {len(packages['flatpak'])} Flatpak " "packages..."
            )
            success &= self._install_flatpak_packages(packages["flatpak"])

        # PIP packages
        if packages.get("pip"):
            console.print(
                f"Installing {len(packages['pip'])} PIP " "packages..."
            )
            success &= self._install_pip_packages(packages["pip"])

        return success

    def _install_apt_packages(self, packages: List[str]) -> bool:
        """Install APT packages"""
        if not packages:
            return True

        # Filter out packages that are already installed
        to_install = []
        for package in packages:
            if not self._is_apt_package_installed(package):
                to_install.append(package)

        if not to_install:
            console.print(
                "[green]✓ All APT packages already " "installed[/green]"
            )
            return True

        console.print(f"Installing {len(to_install)} new APT packages...")

        if self.dry_run:
            preview_pkgs = " ".join(to_install[:10])
            if len(to_install) > 10:
                preview_pkgs += "..."
            console.print(f"[dim]Would install: {preview_pkgs}[/dim]")
            return True

        try:
            # Update package list first
            subprocess.run(
                ["sudo", "apt", "update"], check=True, capture_output=True
            )

            # Install packages in batches to avoid command line too long
            batch_size = 50
            for i in range(0, len(to_install), batch_size):
                batch = to_install[i: i + batch_size]
                cmd = ["sudo", "apt", "install", "-y"] + batch
                result = subprocess.run(cmd, capture_output=True, text=True)

                if result.returncode != 0:
                    console.print(
                        f"[red]Failed to install some APT "
                        f"packages: {result.stderr}[/red]"
                    )
                    return False

            console.print(
                "[green]✓ APT packages installed " "successfully[/green]"
            )
            return True

        except subprocess.CalledProcessError as e:
            console.print(f"[red]Error installing APT packages: {e}[/red]")
            return False

    def _install_snap_packages(self, packages: List[str]) -> bool:
        """Install Snap packages"""
        if not packages:
            return True

        if self.dry_run:
            console.print(
                f"[dim]Would install {len(packages)} snap " "packages[/dim]"
            )
            return True

        try:
            for package in packages:
                if not self._is_snap_package_installed(package):
                    console.print(f"Installing snap: {package}")
                    subprocess.run(
                        ["sudo", "snap", "install", package],
                        check=True,
                        capture_output=True,
                    )

            console.print(
                "[green]✓ Snap packages installed " "successfully[/green]"
            )
            return True

        except subprocess.CalledProcessError as e:
            console.print(
                f"[red]Error installing Snap packages: " f"{e}[/red]"
            )
            return False

    def _install_flatpak_packages(self, packages: List[str]) -> bool:
        """Install Flatpak packages"""
        if not packages:
            return True

        if self.dry_run:
            console.print(
                f"[dim]Would install {len(packages)} flatpak " "packages[/dim]"
            )
            return True

        try:
            for package in packages:
                console.print(f"Installing flatpak: {package}")
                subprocess.run(
                    ["flatpak", "install", "-y", package],
                    check=True,
                    capture_output=True,
                )

            console.print(
                "[green]✓ Flatpak packages installed " "successfully[/green]"
            )
            return True

        except subprocess.CalledProcessError as e:
            console.print(
                f"[red]Error installing Flatpak packages: " f"{e}[/red]"
            )
            return False

    def _install_pip_packages(self, packages: List[str]) -> bool:
        """Install PIP packages"""
        if not packages:
            return True

        if self.dry_run:
            console.print(
                f"[dim]Would install {len(packages)} pip " "packages[/dim]"
            )
            return True

        try:
            # Install packages
            cmd = ["pip", "install"] + packages
            subprocess.run(cmd, check=True, capture_output=True)

            console.print(
                "[green]✓ PIP packages installed " "successfully[/green]"
            )
            return True

        except subprocess.CalledProcessError as e:
            console.print(f"[red]Error installing PIP packages: " f"{e}[/red]")
            return False

    def _restore_dotfiles(self, dotfiles: Dict[str, str]) -> bool:
        """Restore dotfiles"""
        if not dotfiles:
            return True

        console.print(
            f"[bold blue]📝 Restoring {len(dotfiles)} "
            "dotfiles...[/bold blue]"
        )

        if self.dry_run:
            console.print(
                f"[dim]Would restore: " f"{', '.join(dotfiles.keys())}[/dim]"
            )
            return True

        try:
            for filename, content in dotfiles.items():
                file_path = self.home_dir / filename

                # Create directory if needed
                file_path.parent.mkdir(parents=True, exist_ok=True)

                # Backup existing file
                if file_path.exists():
                    backup_path = file_path.with_suffix(
                        file_path.suffix + ".envforge-backup"
                    )
                    file_path.rename(backup_path)
                    console.print(
                        f"Backed up existing {filename} to "
                        f"{backup_path.name}"
                    )

                # Write new content
                with open(file_path, "w") as f:
                    f.write(content)

                console.print(f"✓ Restored {filename}")

            console.print("[green]✓ Dotfiles restored successfully[/green]")
            return True

        except Exception as e:
            console.print(f"[red]Error restoring dotfiles: {e}[/red]")
            return False

    def _restore_vscode_extensions(self, extensions: List[str]) -> bool:
        """Restore VS Code extensions"""
        if not extensions:
            return True

        console.print(
            f"[bold blue]🔌 Restoring {len(extensions)} VS Code "
            "extensions...[/bold blue]"
        )

        if self.dry_run:
            preview_ext = ", ".join(extensions[:5])
            if len(extensions) > 5:
                preview_ext += "..."
            console.print(f"[dim]Would install: {preview_ext}[/dim]")
            return True

        try:
            for extension in extensions:
                console.print(f"Installing extension: {extension}")
                subprocess.run(
                    ["code", "--install-extension", extension],
                    check=True,
                    capture_output=True,
                )

            console.print(
                "[green]✓ VS Code extensions installed " "successfully[/green]"
            )
            return True

        except subprocess.CalledProcessError as e:
            console.print(
                f"[red]Error installing VS Code extensions: " f"{e}[/red]"
            )
            return False

    def _is_apt_package_installed(self, package: str) -> bool:
        """Check if APT package is installed"""
        try:
            result = subprocess.run(
                ["dpkg", "-l", package],
                capture_output=True,
                text=True,
                check=True,
            )
            return "ii" in result.stdout
        except subprocess.CalledProcessError:
            return False

    def _is_snap_package_installed(self, package: str) -> bool:
        """Check if Snap package is installed"""
        try:
            result = subprocess.run(
                ["snap", "list", package],
                capture_output=True,
                text=True,
                check=True,
            )
            return package in result.stdout
        except subprocess.CalledProcessError:
            return False


# Global restorer instance
restorer = EnvironmentRestorer()