# Contributing to EnvForge

🎉 Thank you for considering contributing to EnvForge!

## 🚀 Quick Start

1. **Fork** the repository
2. **Clone** your fork: `git clone https://github.com/YOUR-USERNAME/envforge.git`
3. **Create** a virtual environment: `python -m venv .venv && source .venv/bin/activate`
4. **Install** dependencies: `pip install -e .`
5. **Create** a branch: `git checkout -b feature/your-feature-name`

## 🧪 Testing

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run with coverage
pytest --cov=src/envforge
```

## 📝 Code Style

- Follow PEP 8
- Use type hints where possible
- Write docstrings for functions and classes
- Keep functions focused and small

## 🐛 Reporting Issues

- Use the issue templates
- Include your OS and Python version
- Provide steps to reproduce
- Include error messages and logs

## 💡 Feature Requests

- Check existing issues first
- Use the feature request template
- Explain the use case clearly
- Consider implementation approach

## 📦 Pull Requests

- Keep PRs focused on one feature/fix
- Update tests and documentation
- Ensure CI passes
- Link to relevant issues

## 🏷️ Commit Messages
Use conventional commits:

- `feat`: new features
- `fix`: bug fixes
- `docs`: documentation changes
- `test`: testing changes
- `refactor`: code refactoring

Example: `feat: add Windows support for package detection`

## 🎯 Areas We Need Help

- **Multi-OS Support**: Windows/macOS compatibility
- **Package Managers**: Homebrew, Chocolatey, etc.
- **Testing**: Unit and integration tests
- **Documentation**: Examples and guides
- **GUI**: Desktop interface (PyQt6)

## 📞 Getting Help

- GitHub Discussions for questions
- Issues for bugs and features
- Email: amorimbernardogame@gmail.com

Thanks for contributing! 🚀
