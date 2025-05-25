"""Basic tests for EnvForge"""
import pytest
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock
from envforge.cli.main import cli
from click.testing import CliRunner


def test_cli_help():
    """Test that CLI shows help"""
    runner = CliRunner()
    result = runner.invoke(cli, ['--help'])
    assert result.exit_code == 0
    assert 'EnvForge' in result.output


def test_cli_version():
    """Test CLI version command"""
    runner = CliRunner()
    result = runner.invoke(cli, ['--version'])
    assert result.exit_code == 0


def test_init_command():
    """Test init command"""
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ['init'])
        assert result.exit_code == 0


def test_list_command_empty():
    """Test list command with no environments"""
    runner = CliRunner()
    with runner.isolated_filesystem():
        # Mock storage directly in the main module where it's used
        with patch('envforge.cli.main.storage') as mock_storage:
            mock_storage.list_snapshots.return_value = []
            
            result = runner.invoke(cli, ['list'])
            assert result.exit_code == 0
            assert 'No environments found' in result.output


def test_list_command_with_data():
    """Test list command with existing environments"""
    runner = CliRunner()
    with runner.isolated_filesystem():
        # Mock storage with sample data
        with patch('envforge.cli.main.storage') as mock_storage:
            mock_storage.list_snapshots.return_value = [
                {
                    'name': 'test-env',
                    'created_at': '2025-05-23T20:30:00',
                    'file': '/tmp/test-env.json'
                }
            ]
            
            result = runner.invoke(cli, ['list'])
            assert result.exit_code == 0
            assert 'Available Environments' in result.output
            assert 'test-env' in result.output


def test_status_command():
    """Test status command"""
    runner = CliRunner()
    result = runner.invoke(cli, ['status'])
    assert result.exit_code == 0
