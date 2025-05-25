"""
Configuration management for EnvForge
"""

from pathlib import Path
from typing import Any, Dict

import yaml


class Config:
    def __init__(self):
        self.home_dir = Path.home()
        self.config_dir = self.home_dir / ".envforge"
        self.snapshots_dir = self.config_dir / "snapshots"
        self.config_file = self.config_dir / "config.yaml"

        # Create directories if they don't exist
        self.config_dir.mkdir(exist_ok=True)
        self.snapshots_dir.mkdir(exist_ok=True)

        # Load or create default config
        self.settings = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file or create default"""
        if self.config_file.exists():
            with open(self.config_file, "r") as f:
                return yaml.safe_load(f) or {}
        else:
            # Create default config
            default_config = {
                "version": "0.1.0",
                "capture": {
                    "include_dotfiles": True,
                    "include_packages": True,
                    "include_vscode_extensions": True,
                    "backup_ssh_keys": False,  # Security: disabled by default
                },
                "storage": {
                    "local_only": True,
                    "git_sync": False,
                    "cloud_providers": [],
                },
            }
            self.save_config(default_config)
            return default_config

    def save_config(self, config: Dict[str, Any] = None):
        """Save configuration to file"""
        config_to_save = config or self.settings
        with open(self.config_file, "w") as f:
            yaml.dump(config_to_save, f, default_flow_style=False)

    def get(self, key: str, default=None):
        """Get configuration value"""
        keys = key.split(".")
        value = self.settings
        for k in keys:
            value = value.get(k, {}) if isinstance(value, dict) else default
        return value if value != {} else default


# Global config instance
config = Config()