"""
Local storage management for EnvForge
"""

import json
from datetime import datetime
from typing import Any, Dict, List

from ..core.config import config


class LocalStorage:
    def __init__(self):
        self.snapshots_dir = config.snapshots_dir

    def save_snapshot(self, name: str, data: Dict[str, Any]) -> bool:
        """Save a snapshot to local storage"""
        try:
            # Add metadata
            data["metadata"] = {
                "name": name,
                "created_at": datetime.now().isoformat(),
                "version": "0.1.0",
            }

            # Save to file
            snapshot_file = self.snapshots_dir / f"{name}.json"
            with open(snapshot_file, "w") as f:
                json.dump(data, f, indent=2)

            return True
        except Exception as e:
            print(f"Error saving snapshot: {e}")
            return False

    def load_snapshot(self, name: str) -> Dict[str, Any]:
        """Load a snapshot from local storage"""
        try:
            snapshot_file = self.snapshots_dir / f"{name}.json"
            if not snapshot_file.exists():
                return {}

            with open(snapshot_file, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading snapshot: {e}")
            return {}

    def list_snapshots(self) -> List[Dict[str, Any]]:
        """List all available snapshots"""
        snapshots = []
        try:
            for snapshot_file in self.snapshots_dir.glob("*.json"):
                with open(snapshot_file, "r") as f:
                    data = json.load(f)
                    if "metadata" in data:
                        snapshots.append(
                            {
                                "name": data["metadata"]["name"],
                                "created_at": data["metadata"]["created_at"],
                                "file": str(snapshot_file),
                            }
                        )
        except Exception as e:
            print(f"Error listing snapshots: {e}")

        return sorted(snapshots, key=lambda x: x["created_at"], reverse=True)

    def delete_snapshot(self, name: str) -> bool:
        """Delete a snapshot"""
        try:
            snapshot_file = self.snapshots_dir / f"{name}.json"
            if snapshot_file.exists():
                snapshot_file.unlink()
                return True
            return False
        except Exception as e:
            print(f"Error deleting snapshot: {e}")
            return False


# Global storage instance
storage = LocalStorage()