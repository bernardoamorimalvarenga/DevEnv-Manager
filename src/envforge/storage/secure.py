"""
Secure storage management for EnvForge
Extends local storage with encryption and integrity verification
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from rich.console import Console

from ..core.config import config
from ..core.security import security_manager, SecurityException
from .local import LocalStorage

console = Console()


class SecureStorage(LocalStorage):
    """Secure storage with encryption and integrity verification"""
    
    def __init__(self):
        super().__init__()
        self.security_dir = config.config_dir / "security"
        self.security_dir.mkdir(exist_ok=True)
        self.integrity_file = self.security_dir / "integrity.json"
        self.integrity_db = self._load_integrity_db()
    
    def _load_integrity_db(self) -> Dict[str, str]:
        """Load integrity database"""
        if self.integrity_file.exists():
            try:
                with open(self.integrity_file, 'r') as f:
                    return json.load(f)
            except Exception:
                console.print("[yellow]Warning: Could not load integrity database[/yellow]")
        return {}
    
    def _save_integrity_db(self):
        """Save integrity database"""
        try:
            with open(self.integrity_file, 'w') as f:
                json.dump(self.integrity_db, f, indent=2)
        except Exception as e:
            console.print(f"[red]Error saving integrity database: {e}[/red]")
    
    def save_snapshot(self, name: str, data: Dict[str, Any], 
                     encrypt: bool = None, password: str = None) -> bool:
        """Save a snapshot with security features"""
        try:
            # Use config default if not specified
            if encrypt is None:
                encrypt = config.get("security.encryption", False)
            
            # Apply security filters
            secure_data = security_manager.create_secure_snapshot(
                data,
                encrypt=encrypt,
                filter_sensitive=config.get("security.filter_sensitive", True),
                validate_packages=config.get("security.validate_packages", True)
            )
            
            # Add metadata
            secure_data["metadata"] = {
                "name": name,
                "created_at": datetime.now().isoformat(),
                "version": "0.2.0",
                "encrypted": encrypt,
                "security_version": "1.0"
            }
            
            # Show security warnings
            if "security" in secure_data and secure_data["security"]["warnings"]:
                console.print("[yellow]🔒 Security Warnings:[/yellow]")
                for warning in secure_data["security"]["warnings"]:
                    console.print(f"  • {warning}")
            
            snapshot_file = self.snapshots_dir / f"{name}.json"
            
            if encrypt:
                # Encrypt and save as binary
                encrypted_data, integrity_hash = security_manager.encrypt_data(
                    secure_data, password
                )
                
                # Save encrypted file
                encrypted_file = self.snapshots_dir / f"{name}.enc"
                with open(encrypted_file, 'wb') as f:
                    f.write(encrypted_data)
                
                # Store integrity hash
                self.integrity_db[name] = integrity_hash
                self._save_integrity_db()
                
                # Remove unencrypted file if exists
                if snapshot_file.exists():
                    snapshot_file.unlink()
                
                console.print(f"[green]🔐 Encrypted snapshot saved: {encrypted_file}[/green]")
            else:
                # Save as regular JSON
                with open(snapshot_file, "w") as f:
                    json.dump(secure_data, f, indent=2)
                
                # Calculate and store integrity hash
                with open(snapshot_file, 'rb') as f:
                    file_data = f.read()
                    import hashlib
                    integrity_hash = hashlib.sha256(file_data).hexdigest()
                    self.integrity_db[name] = integrity_hash
                    self._save_integrity_db()
                
                console.print(f"[green]✓ Secure snapshot saved: {snapshot_file}[/green]")
            
            return True
            
        except SecurityException as e:
            console.print(f"[red]Security error: {e}[/red]")
            return False
        except Exception as e:
            console.print(f"[red]Error saving secure snapshot: {e}[/red]")
            return False
    
    def load_snapshot(self, name: str, password: str = None, 
                     verify_integrity: bool = True) -> Dict[str, Any]:
        """Load a snapshot with security verification"""
        try:
            # Check for encrypted file first
            encrypted_file = self.snapshots_dir / f"{name}.enc"
            snapshot_file = self.snapshots_dir / f"{name}.json"
            
            if encrypted_file.exists():
                # Load encrypted snapshot
                with open(encrypted_file, 'rb') as f:
                    encrypted_data = f.read()
                
                # Verify integrity
                if verify_integrity and name in self.integrity_db:
                    expected_hash = self.integrity_db[name]
                    if not security_manager.verify_integrity(encrypted_data, expected_hash):
                        console.print(f"[red]❌ Integrity verification failed for {name}[/red]")
                        return {}
                    console.print(f"[green]✓ Integrity verified for {name}[/green]")
                
                # Decrypt
                data = security_manager.decrypt_data(encrypted_data, password)
                console.print(f"[green]🔓 Decrypted snapshot loaded: {name}[/green]")
                return data
                
            elif snapshot_file.exists():
                # Load regular snapshot
                with open(snapshot_file, 'rb') as f:
                    file_data = f.read()
                
                # Verify integrity
                if verify_integrity and name in self.integrity_db:
                    expected_hash = self.integrity_db[name]
                    if not security_manager.verify_integrity(file_data, expected_hash):
                        console.print(f"[red]❌ Integrity verification failed for {name}[/red]")
                        return {}
                    console.print(f"[green]✓ Integrity verified for {name}[/green]")
                
                # Parse JSON
                data = json.loads(file_data.decode())
                return data
            else:
                console.print(f"[yellow]Snapshot '{name}' not found[/yellow]")
                return {}
                
        except SecurityException as e:
            console.print(f"[red]Security error loading snapshot: {e}[/red]")
            return {}
        except Exception as e:
            console.print(f"[red]Error loading snapshot: {e}[/red]")
            return {}
    
    def list_snapshots(self) -> List[Dict[str, Any]]:
        """List all snapshots with security information"""
        snapshots = []
        try:
            # Find all snapshot files (both encrypted and unencrypted)
            for file_path in self.snapshots_dir.glob("*"):
                if file_path.suffix in ['.json', '.enc']:
                    name = file_path.stem
                    is_encrypted = file_path.suffix == '.enc'
                    
                    # Skip if we already processed this snapshot
                    if any(s['name'] == name for s in snapshots):
                        continue
                    
                    try:
                        # Try to load metadata without full decryption
                        if is_encrypted:
                            # For encrypted files, we can't easily get metadata
                            # without decryption, so we'll use file info
                            created_at = datetime.fromtimestamp(
                                file_path.stat().st_mtime
                            ).isoformat()
                            metadata = {
                                "name": name,
                                "created_at": created_at,
                                "encrypted": True
                            }
                        else:
                            # For unencrypted files, load metadata
                            with open(file_path, 'r') as f:
                                data = json.load(f)
                                metadata = data.get("metadata", {})
                                metadata["encrypted"] = False
                        
                        # Add integrity status
                        metadata["integrity_protected"] = name in self.integrity_db
                        metadata["file"] = str(file_path)
                        
                        snapshots.append(metadata)
                        
                    except Exception as e:
                        console.print(f"[yellow]Warning: Could not read metadata for {name}: {e}[/yellow]")
            
            return sorted(snapshots, key=lambda x: x.get("created_at", ""), reverse=True)
            
        except Exception as e:
            console.print(f"[red]Error listing snapshots: {e}[/red]")
            return []
    
    def delete_snapshot(self, name: str) -> bool:
        """Delete a snapshot and its integrity record"""
        try:
            deleted = False
            
            # Delete encrypted file
            encrypted_file = self.snapshots_dir / f"{name}.enc"
            if encrypted_file.exists():
                encrypted_file.unlink()
                deleted = True
            
            # Delete regular file
            snapshot_file = self.snapshots_dir / f"{name}.json"
            if snapshot_file.exists():
                snapshot_file.unlink()
                deleted = True
            
            # Remove from integrity database
            if name in self.integrity_db:
                del self.integrity_db[name]
                self._save_integrity_db()
            
            if deleted:
                console.print(f"[green]✓ Snapshot '{name}' deleted securely[/green]")
            
            return deleted
            
        except Exception as e:
            console.print(f"[red]Error deleting snapshot: {e}[/red]")
            return False
    
    def get_security_status(self) -> Dict[str, Any]:
        """Get security status of all snapshots"""
        snapshots = self.list_snapshots()
        
        encrypted_count = sum(1 for s in snapshots if s.get("encrypted", False))
        integrity_count = sum(1 for s in snapshots if s.get("integrity_protected", False))
        
        return {
            "total_snapshots": len(snapshots),
            "encrypted_snapshots": encrypted_count,
            "integrity_protected": integrity_count,
            "security_config": security_manager.get_security_config(),
            "snapshots": snapshots
        }
    
    def migrate_to_secure(self, name: str, encrypt: bool = True, 
                         password: str = None) -> bool:
        """Migrate an existing snapshot to secure format"""
        try:
            # Load existing snapshot
            data = super().load_snapshot(name)
            if not data:
                console.print(f"[red]Snapshot '{name}' not found for migration[/red]")
                return False
            
            # Delete old version
            super().delete_snapshot(name)
            
            # Save with security features
            return self.save_snapshot(name, data, encrypt=encrypt, password=password)
            
        except Exception as e:
            console.print(f"[red]Error migrating snapshot: {e}[/red]")
            return False


# Global secure storage instance
secure_storage = SecureStorage()