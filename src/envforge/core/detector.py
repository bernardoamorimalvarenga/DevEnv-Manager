"""
System detection utilities for DevEnv Manager
"""

import os
import subprocess
from pathlib import Path
from typing import Any, Dict, List


class SystemDetector:
    def __init__(self):
        self.home_dir = Path.home()

    def detect_packages(self) -> Dict[str, List[str]]:
        """Detect installed packages"""
        packages = {"apt": [], "snap": [], "flatpak": [], "pip": []}

        # APT packages (manually installed only)
        try:
            result = subprocess.run(
                ["apt-mark", "showmanual"],
                capture_output=True,
                text=True,
                check=True,
            )
            packages["apt"] = (
                result.stdout.strip().split("\n")
                if result.stdout.strip()
                else []
            )
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass

        # Snap packages
        try:
            result = subprocess.run(
                ["snap", "list"], capture_output=True, text=True, check=True
            )
            lines = result.stdout.strip().split("\n")[1:]  # Skip header
            packages["snap"] = [
                line.split()[0] for line in lines if line.strip()
            ]
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass

        # Flatpak packages
        try:
            result = subprocess.run(
                ["flatpak", "list", "--app", "--columns=application"],
                capture_output=True,
                text=True,
                check=True,
            )
            packages["flatpak"] = (
                result.stdout.strip().split("\n")
                if result.stdout.strip()
                else []
            )
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass

        # Global pip packages
        try:
            result = subprocess.run(
                ["pip", "list", "--format=freeze"],
                capture_output=True,
                text=True,
                check=True,
            )
            packages["pip"] = (
                result.stdout.strip().split("\n")
                if result.stdout.strip()
                else []
            )
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass

        return packages

    def detect_dotfiles(self) -> Dict[str, str]:
        """Detect important dotfiles"""
        dotfiles = {}
        important_dotfiles = [
            ".bashrc",
            ".bash_profile",
            ".zshrc",
            ".profile",
            ".vimrc",
            ".gitconfig",
            ".ssh/config",
        ]

        for dotfile in important_dotfiles:
            file_path = self.home_dir / dotfile
            if file_path.exists() and file_path.is_file():
                try:
                    with open(file_path, "r") as f:
                        dotfiles[dotfile] = f.read()
                except Exception as e:
                    print(f"Warning: Could not read {dotfile}: {e}")

        return dotfiles

    def detect_vscode_extensions(self) -> List[str]:
        """Detect VS Code extensions"""
        extensions = []
        try:
            result = subprocess.run(
                ["code", "--list-extensions"],
                capture_output=True,
                text=True,
                check=True,
            )
            extensions = (
                result.stdout.strip().split("\n")
                if result.stdout.strip()
                else []
            )
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass

        return extensions

    def get_system_info(self) -> Dict[str, Any]:
        """Get basic system information"""
        return {
            "os": os.uname().sysname,
            "kernel": os.uname().release,
            "architecture": os.uname().machine,
            "hostname": os.uname().nodename,
            "python_version": os.sys.version.split()[0],
            "shell": os.environ.get("SHELL", "unknown"),
            "user": os.environ.get("USER", "unknown"),
        }


# Global detector instance
detector = SystemDetector()
