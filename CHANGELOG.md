# Changelog

All notable changes to DevEnv Manager will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial public release
- Complete CLI interface with 12+ commands
- Git-based synchronization system
- Package detection for APT, Snap, Flatpak, PIP
- Dotfiles backup and restoration
- VS Code extensions management
- Export/Import functionality
- Environment comparison (diff)
- Dry-run mode for safe previews

### Changed
- N/A

### Deprecated
- N/A

### Removed
- N/A

### Fixed
- Click multiple=True parameter handling in sync push command

### Security
- SSH keys disabled by default
- Automatic backup of existing files
- Private repository recommendations

## [0.1.0] - 2025-05-23

### Added
- Initial MVP release
- Core functionality complete
- Local storage system
- Git synchronization
- Rich CLI interface
