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
        # Mock secure_storage directly in the main module where it's used
        with patch('envforge.cli.main.secure_storage') as mock_storage:
            mock_storage.list_snapshots.return_value = []
            
            result = runner.invoke(cli, ['list'])
            assert result.exit_code == 0
            assert 'No environments found' in result.output


def test_list_command_with_data():
    """Test list command with existing environments"""
    runner = CliRunner()
    with runner.isolated_filesystem():
        # Mock secure_storage with sample data
        with patch('envforge.cli.main.secure_storage') as mock_storage:
            mock_storage.list_snapshots.return_value = [
                {
                    'name': 'test-env',
                    'created_at': '2025-05-23T20:30:00',
                    'file': '/tmp/test-env.json',
                    'encrypted': False,
                    'integrity_protected': True
                }
            ]
            
            result = runner.invoke(cli, ['list'])
            assert result.exit_code == 0
            assert 'Available Environments' in result.output
            assert 'test-env' in result.output


def test_status_command():
    """Test status command"""
    runner = CliRunner()
    with patch('envforge.cli.main.detector') as mock_detector, \
         patch('envforge.cli.main.secure_storage') as mock_storage:
        
        # Mock detector responses
        mock_detector.get_system_info.return_value = {
            'os': 'Linux',
            'kernel': '5.15.0',
            'python_version': '3.12.3'
        }
        mock_detector.detect_packages.return_value = {
            'apt': ['git', 'vim'],
            'pip': ['requests']
        }
        
        # Mock storage security status
        mock_storage.get_security_status.return_value = {
            'total_snapshots': 0,
            'encrypted_snapshots': 0,
            'integrity_protected': 0
        }
        
        result = runner.invoke(cli, ['status'])
        assert result.exit_code == 0
        assert 'System Status' in result.output


def test_security_status_command():
    """Test security status command"""
    runner = CliRunner()
    with patch('envforge.cli.main.secure_storage') as mock_storage:
        mock_storage.get_security_status.return_value = {
            'total_snapshots': 2,
            'encrypted_snapshots': 1,
            'integrity_protected': 2,
            'security_config': {
                'encryption_enabled': False,
                'sensitive_filtering': True,
                'package_validation': True,
                'safe_packages_count': {
                    'apt': 50,
                    'pip': 25
                }
            },
            'snapshots': []
        }
        
        result = runner.invoke(cli, ['security', 'status'])
        assert result.exit_code == 0
        assert 'Security Status Overview' in result.output


def test_capture_command_basic():
    """Test basic capture command"""
    runner = CliRunner()
    with patch('envforge.cli.main.detector') as mock_detector, \
         patch('envforge.cli.main.secure_storage') as mock_storage:
        
        # Mock detector responses
        mock_detector.get_system_info.return_value = {'os': 'Linux'}
        mock_detector.detect_packages.return_value = {
            'apt': ['git'], 'snap': [], 'flatpak': [], 'pip': []
        }
        mock_detector.detect_dotfiles.return_value = {'.bashrc': 'echo hello'}
        mock_detector.detect_vscode_extensions.return_value = []
        
        # Mock storage save
        mock_storage.save_snapshot.return_value = True
        
        result = runner.invoke(cli, ['capture', 'test-env'])
        assert result.exit_code == 0
        assert 'test-env' in result.output
        assert 'captured successfully' in result.output


def test_capture_command_with_encryption():
    """Test capture command with encryption"""
    runner = CliRunner()
    with patch('envforge.cli.main.detector') as mock_detector, \
         patch('envforge.cli.main.secure_storage') as mock_storage:
        
        # Mock detector responses
        mock_detector.get_system_info.return_value = {'os': 'Linux'}
        mock_detector.detect_packages.return_value = {
            'apt': ['git'], 'snap': [], 'flatpak': [], 'pip': []
        }
        mock_detector.detect_dotfiles.return_value = {'.bashrc': 'echo hello'}
        mock_detector.detect_vscode_extensions.return_value = []
        
        # Mock storage save
        mock_storage.save_snapshot.return_value = True
        
        result = runner.invoke(cli, ['capture', 'encrypted-env', '--encrypt', '--password', 'test123'])
        assert result.exit_code == 0
        assert 'encrypted-env' in result.output
        assert 'captured successfully' in result.output


def test_show_command():
    """Test show command"""
    runner = CliRunner()
    with patch('envforge.cli.main.secure_storage') as mock_storage:
        
        mock_storage.load_snapshot.return_value = {
            'system_info': {'os': 'Linux', 'kernel': '5.15.0'},
            'packages': {'apt': ['git', 'vim'], 'pip': ['requests']},
            'security': {
                'encryption_enabled': False,
                'sensitive_filtering': True,
                'package_validation': True,
                'warnings': []
            }
        }
        
        result = runner.invoke(cli, ['show', 'test-env'])
        assert result.exit_code == 0
        assert 'Environment Details' in result.output
        assert 'test-env' in result.output


def test_show_command_not_found():
    """Test show command with non-existent environment"""
    runner = CliRunner()
    with patch('envforge.cli.main.secure_storage') as mock_storage:
        
        mock_storage.load_snapshot.return_value = {}
        
        result = runner.invoke(cli, ['show', 'nonexistent'])
        assert result.exit_code == 0
        assert 'not found' in result.output or 'could not be decrypted' in result.output


def test_delete_command():
    """Test delete command"""
    runner = CliRunner()
    with patch('envforge.cli.main.secure_storage') as mock_storage:
        
        # Mock that snapshot exists
        mock_storage.list_snapshots.return_value = [
            {'name': 'test-env', 'created_at': '2025-05-28T10:00:00'}
        ]
        mock_storage.delete_snapshot.return_value = True
        
        result = runner.invoke(cli, ['delete', 'test-env', '--force'])
        assert result.exit_code == 0
        assert 'deleted successfully' in result.output


def test_export_command():
    """Test export command"""
    runner = CliRunner()
    with runner.isolated_filesystem():
        with patch('envforge.cli.main.secure_storage') as mock_storage:
            
            mock_storage.load_snapshot.return_value = {
                'packages': {'apt': ['git']},
                'metadata': {'name': 'test-env'}
            }
            
            result = runner.invoke(cli, ['export', 'test-env', 'export.json'])
            assert result.exit_code == 0
            assert 'exported' in result.output


def test_import_command():
    """Test import command"""
    runner = CliRunner()
    with runner.isolated_filesystem():
        # Create a test import file
        import json
        test_data = {
            'packages': {'apt': ['git']},
            'metadata': {'name': 'imported-env'}
        }
        with open('import.json', 'w') as f:
            json.dump(test_data, f)
        
        with patch('envforge.cli.main.secure_storage') as mock_storage:
            mock_storage.list_snapshots.return_value = []  # No existing snapshots
            mock_storage.save_snapshot.return_value = True
            
            result = runner.invoke(cli, ['import-env', 'import.json'])
            assert result.exit_code == 0
            assert 'imported' in result.output