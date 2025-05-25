"""Test configuration module"""

import shutil
import tempfile
from pathlib import Path

from envforge.core.config import Config


def test_config_creation():
    """Test config initialization"""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Mock home directory
        config = Config()
        assert config.settings is not None


def test_config_default_values():
    """Test default configuration values"""
    config = Config()
    assert config.get("version") == "0.1.0"
    assert config.get("capture.include_dotfiles") is True
