"""
Security utilities for EnvForge
Handles encryption, filtering, and integrity verification
"""

import hashlib
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os
import getpass

from ..core.config import config


class SecurityManager:
    def __init__(self):
        self.config = config
        self.safe_packages = self._load_safe_packages()
        self.sensitive_patterns = self._load_sensitive_patterns()
        
    def _load_safe_packages(self) -> Dict[str, Set[str]]:
        """Load whitelist of safe packages by package manager"""
        # Default safe packages (can be extended by user config)
        return {
            "apt": {
                # Core system packages
                "git", "curl", "wget", "vim", "nano", "tree", "htop",
                "build-essential", "python3", "python3-pip", "nodejs", "npm",
                "docker.io", "docker-compose", "openssh-client",
                # Development tools
                "code", "sublime-text", "atom", "slack-desktop",
                "firefox", "chromium-browser", "vlc", "gimp",
                # Languages and runtimes
                "golang", "rustc", "openjdk-11-jdk", "ruby", "php",
                "postgresql", "mysql-server", "redis-server", "nginx",
                # Utilities
                "zip", "unzip", "tar", "gzip", "jq", "xmlstarlet",
                "ffmpeg", "imagemagick", "pandoc"
            },
            "snap": {
                "code", "discord", "telegram-desktop", "slack",
                "firefox", "chromium", "vlc", "gimp", "blender",
                "docker", "kubectl", "helm", "postman", "insomnia"
            },
            "flatpak": {
                "org.mozilla.Firefox", "org.chromium.Chromium",
                "com.discordapp.Discord", "org.telegram.desktop",
                "org.videolan.VLC", "org.gimp.GIMP", "org.blender.Blender"
            },
            "pip": {
                # Common development packages
                "requests", "flask", "django", "fastapi", "sqlalchemy",
                "pandas", "numpy", "matplotlib", "seaborn", "jupyter",
                "pytest", "black", "flake8", "mypy", "isort",
                "click", "rich", "pyyaml", "python-dotenv"
            }
        }
    
    def _load_sensitive_patterns(self) -> List[re.Pattern]:
        """Load regex patterns for sensitive data detection"""
        patterns = [
            # API Keys and tokens
            r'["\']?(?:api[_-]?key|token|secret)["\']?\s*[:=]\s*["\']?([a-zA-Z0-9_-]{20,})["\']?',
            # AWS Keys
            r'AKIA[0-9A-Z]{16}',
            r'(?:aws_secret_access_key|AWS_SECRET_ACCESS_KEY)\s*[:=]\s*["\']?([a-zA-Z0-9+/]{40})["\']?',
            # GitHub tokens
            r'gh[pousr]_[A-Za-z0-9_]{36,255}',
            # SSH private keys
            r'-----BEGIN (?:RSA |EC |DSA )?PRIVATE KEY-----',
            # Passwords
            r'["\']?(?:password|passwd|pwd)["\']?\s*[:=]\s*["\']?([^"\'\s]{8,})["\']?',
            # Database URLs
            r'(?:postgres|mysql|mongodb)://[^\s"\']+',
            # Email addresses (sometimes sensitive)
            r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
            # IP addresses (private ranges)
            r'(?:192\.168\.|10\.|172\.(?:1[6-9]|2[0-9]|3[01])\.)\d{1,3}\.\d{1,3}',
            # Common secret formats
            r'["\']?(?:client[_-]?secret|private[_-]?key|secret[_-]?key)["\']?\s*[:=]\s*["\']?([a-zA-Z0-9_-]{20,})["\']?'
        ]
        return [re.compile(pattern, re.IGNORECASE) for pattern in patterns]
    
    def generate_key(self, password: str = None) -> bytes:
        """Generate encryption key from password"""
        if not password:
            password = getpass.getpass("Enter encryption password: ")
        
        # Use a fixed salt for reproducibility (in real app, store salt separately)
        salt = b'envforge_salt_v1'
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key
    
    def encrypt_data(self, data: Dict[str, Any], password: str = None) -> Tuple[bytes, str]:
        """Encrypt snapshot data"""
        try:
            # Validate input data
            if data is None:
                raise SecurityException("Cannot encrypt None data")
            
            if not isinstance(data, dict):
                raise SecurityException("Data must be a dictionary")
            
            key = self.generate_key(password)
            fernet = Fernet(key)
            
            # Convert to JSON and encrypt
            json_data = json.dumps(data, indent=2)
            encrypted_data = fernet.encrypt(json_data.encode())
            
            # Generate integrity hash
            integrity_hash = hashlib.sha256(encrypted_data).hexdigest()
            
            return encrypted_data, integrity_hash
        except SecurityException:
            # Re-raise SecurityException as-is
            raise
        except Exception as e:
            raise SecurityException(f"Encryption failed: {e}")
    
    def decrypt_data(self, encrypted_data: bytes, password: str = None) -> Dict[str, Any]:
        """Decrypt snapshot data"""
        try:
            key = self.generate_key(password)
            fernet = Fernet(key)
            
            # Decrypt and parse JSON
            decrypted_bytes = fernet.decrypt(encrypted_data)
            json_data = decrypted_bytes.decode()
            data = json.loads(json_data)
            
            return data
        except Exception as e:
            raise SecurityException(f"Decryption failed: {e}")
    
    def verify_integrity(self, data: bytes, expected_hash: str) -> bool:
        """Verify data integrity using hash"""
        actual_hash = hashlib.sha256(data).hexdigest()
        return actual_hash == expected_hash
    
    def filter_sensitive_data(self, content: str, filename: str = "") -> Tuple[str, List[str]]:
        """Filter sensitive data from content and return filtered content + warnings"""
        filtered_content = content
        warnings = []
        
        for pattern in self.sensitive_patterns:
            matches = pattern.findall(content)
            if matches:
                # Replace sensitive data with placeholder
                filtered_content = pattern.sub('[FILTERED_SENSITIVE_DATA]', filtered_content)
                warnings.append(f"Sensitive data filtered from {filename or 'content'}")
        
        return filtered_content, warnings
    
    def validate_packages(self, packages: Dict[str, List[str]]) -> Dict[str, Any]:
        """Validate packages against whitelist and return validation report"""
        report = {
            "safe_packages": {},
            "unsafe_packages": {},
            "warnings": [],
            "blocked_count": 0,
            "total_count": 0
        }
        
        for pkg_type, pkg_list in packages.items():
            if pkg_type not in self.safe_packages:
                report["warnings"].append(f"Unknown package type: {pkg_type}")
                continue
            
            safe_set = self.safe_packages[pkg_type]
            safe_pkgs = []
            unsafe_pkgs = []
            
            for pkg in pkg_list:
                report["total_count"] += 1
                # Extract package name (remove version info)
                pkg_name = pkg.split('=')[0].split('==')[0].strip()
                
                if pkg_name in safe_set:
                    safe_pkgs.append(pkg)
                else:
                    unsafe_pkgs.append(pkg)
                    report["blocked_count"] += 1
            
            if safe_pkgs:
                report["safe_packages"][pkg_type] = safe_pkgs
            if unsafe_pkgs:
                report["unsafe_packages"][pkg_type] = unsafe_pkgs
        
        return report
    
    def create_secure_snapshot(self, data: Dict[str, Any], encrypt: bool = False, 
                             filter_sensitive: bool = True, 
                             validate_packages: bool = True) -> Dict[str, Any]:
        """Create a secure snapshot with all security features applied"""
        secure_data = data.copy()
        security_report = {
            "encryption_enabled": encrypt,
            "sensitive_filtering": filter_sensitive,
            "package_validation": validate_packages,
            "warnings": [],
            "filtered_files": [],
            "package_report": None
        }
        
        # 1. Package validation
        if validate_packages and "packages" in secure_data:
            pkg_report = self.validate_packages(secure_data["packages"])
            security_report["package_report"] = pkg_report
            
            # Only include safe packages
            secure_data["packages"] = pkg_report["safe_packages"]
            
            if pkg_report["blocked_count"] > 0:
                security_report["warnings"].append(
                    f"Blocked {pkg_report['blocked_count']} unsafe packages"
                )
        
        # 2. Sensitive data filtering
        if filter_sensitive and "dotfiles" in secure_data:
            filtered_dotfiles = {}
            for filename, content in secure_data["dotfiles"].items():
                filtered_content, warnings = self.filter_sensitive_data(content, filename)
                filtered_dotfiles[filename] = filtered_content
                
                if warnings:
                    security_report["warnings"].extend(warnings)
                    security_report["filtered_files"].append(filename)
            
            secure_data["dotfiles"] = filtered_dotfiles
        
        # 3. Add security metadata
        secure_data["security"] = security_report
        
        return secure_data
    
    def get_security_config(self) -> Dict[str, Any]:
        """Get current security configuration"""
        return {
            "encryption_enabled": self.config.get("security.encryption", False),
            "sensitive_filtering": self.config.get("security.filter_sensitive", True),
            "package_validation": self.config.get("security.validate_packages", True),
            "safe_packages_count": {
                pkg_type: len(pkgs) for pkg_type, pkgs in self.safe_packages.items()
            }
        }
    
    def update_safe_packages(self, pkg_type: str, packages: List[str], 
                           action: str = "add") -> bool:
        """Update safe packages list"""
        if pkg_type not in self.safe_packages:
            self.safe_packages[pkg_type] = set()
        
        if action == "add":
            self.safe_packages[pkg_type].update(packages)
        elif action == "remove":
            self.safe_packages[pkg_type] -= set(packages)
        
        # Save to config
        safe_packages_dict = {
            pkg_type: list(pkgs) for pkg_type, pkgs in self.safe_packages.items()
        }
        self.config.settings.setdefault("security", {})["safe_packages"] = safe_packages_dict
        self.config.save_config()
        
        return True


class SecurityException(Exception):
    """Custom exception for security-related errors"""
    pass


# Global security manager instance
security_manager = SecurityManager()