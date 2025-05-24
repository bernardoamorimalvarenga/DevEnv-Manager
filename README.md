# 🚀 DevEnv Manager

**Save, sync and restore complete development environments in minutes**

![PyPI](https://img.shields.io/pypi/v/devenv-manager)
![GitHub Stars](https://img.shields.io/github/stars/bernardoamorimalvarenga/devenv-manager)
![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Platform](https://img.shields.io/badge/platform-Linux-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Status](https://img.shields.io/badge/status-stable-brightgreen.svg)

---

## 🎯 **What Is It?**

DevEnv Manager is a CLI tool that solves one of developers' biggest problems: **reconfiguring development environments from scratch**.

Instead of spending days installing packages, configuring dotfiles and extensions every time you:
- 💻 Buy a new laptop
- 🔄 Format your system  
- 👥 Need to standardize the team
- 🏠 Want to sync home/work

**You simply restore everything automatically!**

---

## 🆚 **DevEnv Manager vs Other Tools**

| | DevEnv Manager | Git/GitHub | Docker | Dotfiles Repos |
|---|---|---|---|---|
| **What it manages** | 🖥️ **Complete environment** | 📝 Source code | 📦 Isolated containers | 📄 Config files only |
| **Installs packages** | ✅ 271 APT packages | ❌ | ❌ | ❌ |
| **Configures system** | ✅ Dotfiles + extensions | ❌ | ❌ | ✅ Configs only |
| **Synchronization** | ✅ Bidirectional Git | ✅ Code only | ❌ | ✅ Configs only |
| **Use case** | 🛠️ Complete personal setup | 📂 Code projects | 🚀 App deployment | ⚙️ Basic configs |

### **DevEnv Manager vs devenv.sh**

| | DevEnv Manager | devenv.sh |
|---|---|---|
| **Approach** | 📸 Capture existing environment | 📝 Declare from scratch |
| **Technology** | 🐍 Python + Linux tools | ❄️ Nix ecosystem |
| **Complexity** | 🟢 Simple - one command | 🔴 Complex - requires Nix |
| **Installation** | `pip install devenv-manager` | Nix + configuration |
| **Command** | `devm capture`, `devm restore` | `devenv shell` |
| **Target audience** | 👨‍💻 Beginner/intermediate devs | 🧙‍♂️ Advanced Nix users |
| **Use case** | 🔄 Backup/sync existing environments | 🏗️ Reproducible environments |
| **Learning curve** | 5 minutes | Weeks (Nix) |

### **Practical Example:**

**❌ Current Situation (2 days of work):**
```bash
# New/formatted laptop:
sudo apt update && sudo apt install git curl vim...    # 271+ packages manually
code --install-extension ms-python.python...          # 15+ VS Code extensions  
cp dotfiles/.bashrc ~/.bashrc                         # Configure terminal
git config --global user.name...                      # Git configs
# ... hundreds of manual steps
```

**✅ With DevEnv Manager (30 minutes):**
```bash
pip install devenv-manager
devm restore "my-complete-environment"
# ☕ Go grab a coffee - everything automated!
```

---

## 🚀 **Installation**

### **Method 1: Direct Installation (Recommended)**
```bash
pip install devenv-manager
```

### **Method 2: Manual Installation**
```bash
# Clone the repository
git clone https://github.com/bernardoamorimalvarenga/devenv-manager.git
cd devenv-manager

# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -e .

# Test installation
devm --help
```

### **System Requirements:**
- 🐧 **Linux** (Ubuntu 20.04+, Debian 10+, Arch, Fedora)
- 🐍 **Python 3.8+**
- 🔑 **sudo** (for package installation)
- 📦 **git** (for synchronization)

---

## 📋 **Complete Usage Guide**

### **1. Initial Setup**

```bash
# Initialize DevEnv Manager
devm init

# ✅ Output:
# 🚀 DevEnv Manager initialized successfully!
# Config stored in: /home/user/.devenv
```

### **2. Capture Your Current Environment**

```bash
# Capture everything that's installed and configured
devm capture "my-setup-$(date +%Y%m%d)"

# ✅ Example output:
# 📸 Capturing environment: my-setup-20241201
# ✓ Detecting system configuration...
# 
# ┏━━━━━━━━━━━━━━━━━━━━┳━━━━━━━┓
# ┃ Component          ┃ Count ┃
# ┡━━━━━━━━━━━━━━━━━━━━╇━━━━━━━┩
# │ APT Packages       │ 271   │
# │ Snap Packages      │ 26    │
# │ Flatpak Packages   │ 3     │
# │ PIP Packages       │ 45    │
# │ Dotfiles           │ 8     │
# │ VS Code Extensions │ 23    │
# └────────────────────┴───────┘
# ✓ Environment 'my-setup-20241201' captured successfully!
```

### **3. List Saved Environments**

```bash
# List all captured environments
devm list

# ✅ Example output:
# ┏━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┓
# ┃ Name                 ┃ Created         ┃ File                ┃
# ┡━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━┩
# │ my-setup-20241201    │ 2024-12-01 14:30│ my-setup-20241201.json │
# │ work-environment     │ 2024-11-28 09:15│ work-environment.json  │
# │ complete-setup       │ 2024-11-25 16:45│ complete-setup.json     │
# └──────────────────────┴─────────────────┴─────────────────────────┘
```

### **4. View Environment Details**

```bash
# See what a specific environment contains
devm show "my-setup-20241201"

# ✅ Example output:
# 📋 Environment Details: my-setup-20241201
# 
# ┏━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃ Property           ┃ Value                        ┃
# ┡━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
# │ Os                 │ Linux                        │
# │ Kernel             │ 5.15.0-91-generic           │
# │ Architecture       │ x86_64                       │
# │ Python Version     │ 3.12.3                      │
# │ Shell              │ /bin/bash                    │
# └────────────────────┴─────────────────────────────┘
# 
# ┏━━━━━━━━━━━━━━━━━━━━┳━━━━━━━┓
# ┃ Type               ┃ Count ┃
# ┡━━━━━━━━━━━━━━━━━━━━╇━━━━━━━┩
# │ APT                │ 271   │
# │ SNAP               │ 26    │
# │ FLATPAK            │ 3     │
# │ PIP                │ 45    │
# └────────────────────┴───────┘
```

### **5. Restore an Environment**

#### **Safe Preview (Dry Run):**
```bash
# See what will be done WITHOUT applying changes
devm restore "my-setup-20241201" --dry-run

# ✅ Example output:
# 🔍 DRY RUN MODE - No changes will be made
# 📦 Restoring packages...
# Would install 45 new APT packages
# Would install: git vim curl nodejs python3-pip code...
# 📝 Would restore 8 dotfiles
# 🔌 Would install 12 new VS Code extensions
# ✓ Dry run completed successfully!
```

#### **Actual Restoration:**
```bash
# Restore the environment (WILL INSTALL PACKAGES)
devm restore "my-setup-20241201"

# ✅ Interactive process:
# 🔄 Restoring environment: my-setup-20241201
# 
# ┏━━━━━━━━━━━━━━━━━━━━┳━━━━━━━┓
# ┃ Type               ┃ Count ┃
# ┡━━━━━━━━━━━━━━━━━━━━╇━━━━━━━┩
# │ APT                │ 45    │
# │ SNAP               │ 8     │
# │ PIP                │ 12    │
# └────────────────────┴───────┘
# 
# ⚠️  This will install 65 packages and may modify your system.
# Do you want to continue? [y/N]: y
# 
# 📦 Installing APT packages...
# ✓ APT packages installed successfully
# 📝 Restoring dotfiles...
# Backed up existing .bashrc to .bashrc.devenv-backup
# ✓ Restored .bashrc
# ✓ Restored .vimrc
# 🔌 Installing VS Code extensions...
# ✓ VS Code extensions installed successfully
# ✓ Environment restored successfully!
```

---

## 🔄 **Git Synchronization (Multi-machine)**

### **Initial Setup (One time)**

```bash
# Configure synchronization with private repository
devm sync setup git@github.com:your-username/devenv-private.git

# ✅ Output:
# 🔧 Setting up git sync with git@github.com:your-username/devenv-private.git
# 
# ╭─ Sync Ready ─╮
# │ Git sync setup complete! │
# │                          │
# │ Repository: git@github.com:your-username/devenv-private.git │
# │ Branch: main             │
# │                          │
# │ Use 'devm sync push' to upload environments │
# │ Use 'devm sync pull' to download environments │
# ╰──────────────╯
```

### **Pushing Environments**

```bash
# Push all environments to repository
devm sync push

# Push only a specific environment
devm sync push -e "my-setup-20241201"

# Push multiple environments
devm sync push -e "environment1" -e "environment2"

# ✅ Example output:
# 📤 Pushing specific environments: my-setup-20241201
# ✓ Successfully pushed 1 specific environments
```

### **Pulling Environments**

```bash
# Download environments from repository
devm sync pull

# ✅ Example output:
# 📥 Pulling environments from remote...
# ✓ Imported work-environment
# ✓ Imported home-setup
# ✓ Successfully imported 2 environments
```

### **Sync Status**

```bash
# View sync status
devm sync status

# ✅ Example output:
# ┏━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃ Property           ┃ Value                                               ┃
# ┡━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
# │ Status             │ ✓ Enabled                                          │
# │ Remote URL         │ git@github.com:your-username/devenv-private.git   │
# │ Branch             │ main                                               │
# │ Uncommitted Changes │ No                                                │
# │ Last Commit        │ abc123 - Sync 2 environments                      │
# └────────────────────┴────────────────────────────────────────────────────┘
```

---

## 💼 **Practical Use Cases**

### **🆕 Case 1: New Laptop**
```bash
# On old machine:
devm capture "my-complete-setup"
devm sync push

# On new machine:
pip install devenv-manager
devm init
devm sync setup git@github.com:your-username/devenv-private.git
devm sync pull
devm restore "my-complete-setup"
# ☕ 30 minutes later: identical environment!
```

### **👥 Case 2: Team Onboarding**
```bash
# Company setup (done once by tech lead):
devm capture "company-dev-env-2024"  
devm sync push

# New developer:
devm sync pull
devm restore "company-dev-env-2024"
# 🎉 Standardized environment automatically!
```

### **🏠 Case 3: Home/Work Sync**
```bash
# At work:
devm capture "work-setup"
devm sync push

# At home:
devm sync pull
devm restore "work-setup" 
# 🔄 Same environment at home!
```

### **🔄 Case 4: Backup/Disaster Recovery**
```bash
# Regular backup:
devm capture "backup-$(date +%Y%m%d)"
devm sync push

# After problem/formatting:
devm sync pull
devm list  # See available backups
devm restore "backup-20241201"
# 🛡️ Environment restored!
```

---

## 📊 **Available Commands**

### **Basic Commands:**
```bash
devm init                    # Initialize DevEnv Manager
devm capture "name"          # Capture current environment
devm list                    # List saved environments
devm show "name"             # Show environment details  
devm restore "name"          # Restore environment
devm delete "name"           # Delete environment
devm status                  # Current system status
```

### **Sync Commands:**
```bash
devm sync setup <repo-url>   # Configure Git synchronization
devm sync push               # Push all environments
devm sync push -e "name"     # Push specific environment
devm sync pull               # Download environments from repository
devm sync status             # Synchronization status
```

### **Utility Commands:**
```bash
devm export "name" file.json    # Export to file
devm import-env file.json       # Import from file
devm diff "env1" "env2"         # Compare environments
devm clean                      # Clean old backups
```

### **Useful Options:**
```bash
devm restore "name" --dry-run     # Preview without applying changes
devm restore "name" --force       # Skip confirmations
devm delete "name" --force        # Delete without confirmation
```

---

## 🎯 **What Gets Captured**

### **📦 System Packages:**
- **APT packages** (manually installed only)
- **Snap packages** 
- **Flatpak packages**
- **PIP packages** (global)

### **⚙️ Configurations:**
- **Important dotfiles**: `.bashrc`, `.bash_profile`, `.zshrc`, `.profile`
- **Tool configs**: `.vimrc`, `.gitconfig`
- **SSH config**: `.ssh/config` (optional, disabled by default)

### **🔌 Extensions and Tools:**
- **VS Code**: All installed extensions
- **System info**: OS, kernel, architecture, Python version

### **Example Snapshot (JSON):**
```json
{
  "metadata": {
    "name": "my-setup-20241201",
    "created_at": "2024-12-01T14:30:00",
    "version": "0.1.0"
  },
  "system_info": {
    "os": "Linux",
    "kernel": "5.15.0-91-generic",
    "architecture": "x86_64",
    "python_version": "3.12.3"
  },
  "packages": {
    "apt": ["git", "vim", "curl", "nodejs", "python3-pip"],
    "snap": ["code", "discord", "telegram-desktop"],
    "pip": ["requests", "flask", "django"]
  },
  "dotfiles": {
    ".bashrc": "# Content of .bashrc...",
    ".vimrc": "# Vim configurations..."
  },
  "vscode_extensions": [
    "ms-python.python",
    "ms-vscode.vscode-json"
  ]
}
```

---

## 🔒 **Security**

### **✅ Secure Settings:**
- **SSH keys** not captured by default
- **Automatic backups** of existing files before replacing
- **Dry-run mode** for safe preview
- **Confirmations** before important changes
- **Private repositories** recommended for sync

### **⚠️ Important Precautions:**
- **Use private repositories** for sensitive data
- **Review snapshots** before sharing
- **Dotfiles may contain personal information**
- **Always test with --dry-run** first

### **🛡️ Best Practices:**
```bash
# ✅ Use private repository
devm sync setup git@github.com:your-username/devenv-PRIVATE.git

# ✅ Always preview first
devm restore "environment" --dry-run

# ✅ Manual backup before major changes
cp ~/.bashrc ~/.bashrc.backup-$(date +%s)

# ✅ Review what will be installed
devm show "environment"
```

---

## 🚀 **Performance**

### **Typical Times:**
- **Capture**: ~30 seconds (271 packages + configs)
- **Restore APT**: ~15 minutes (271 packages)
- **Restore Snap**: ~5 minutes (26 packages)
- **Dotfiles**: ~1 second
- **VS Code extensions**: ~2 minutes

### **Sizes:**
- **Snapshot JSON**: ~16KB per environment
- **Sync repository**: ~1MB (10 environments)

---

## 🐛 **Troubleshooting**

### **Common Issues:**

#### **"Permission denied" during restore:**
```bash
# Make sure you have sudo
sudo echo "test"

# Execute with confirmation
devm restore "environment" --force
```

#### **"Git sync failed":**
```bash
# Check if repository is private and you have access
git clone git@github.com:your-username/devenv-private.git

# Reconfigure if necessary
devm sync setup git@github.com:your-username/devenv-private.git
```

#### **"VS Code extensions failed":**
```bash
# Make sure VS Code is installed
code --version

# Install manually if necessary
devm show "environment"  # See extensions list
```

### **Logs and Debug:**
```bash
# View detailed status
devm status

# Check config files
ls -la ~/.devenv/

# Preview before applying
devm restore "environment" --dry-run
```

---

## 🤝 **Contributing**

Contributions are welcome! 

### **How to Contribute:**
1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/new-feature`)
3. **Commit** your changes (`git commit -am 'Add new feature'`)
4. **Push** to the branch (`git push origin feature/new-feature`)
5. **Open** a Pull Request

### **Areas That Need Help:**
- **Support for other distros** (CentOS, OpenSUSE)
- **Additional package managers** (brew, chocolatey)
- **Automated testing**
- **Documentation**
- **Graphical interface**

---

## 🗺️ **Roadmap**

### **v0.2.0 - Security** (Next 4 weeks)
- [ ] Snapshot encryption
- [ ] Safe packages list (whitelist)
- [ ] Sensitive data filtering
- [ ] Integrity verification

### **v0.3.0 - Multi-OS** (8 weeks)
- [ ] Windows support (WSL)
- [ ] macOS support
- [ ] Homebrew support
- [ ] Chocolatey support

### **v1.0.0 - GUI and Cloud** (12 weeks)
- [ ] Graphical interface (PyQt6)
- [ ] Cloud storage (Google Drive, Dropbox)
- [ ] Community templates
- [ ] Pro version with advanced features

---

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 **Author**

**Bernardo Amorim Alvarenga**
- GitHub: [@bernardoamorimalvarenga](https://github.com/bernardoamorimalvarenga)
- Email: amorimbernardogame@gmail.com

---

## 🙏 **Acknowledgments**

- **Click** - Fantastic CLI framework
- **Rich** - Beautiful and colorful interface  
- **Git** - Robust sync system
- **Python Community** - Amazing tools

---

## ⭐ **Like the Project?**

If DevEnv Manager helped you, consider:
- ⭐ **Star** the GitHub repository
- 🐛 **Report bugs** or **suggest improvements**
- 📢 **Share** with other developers
- 🤝 **Contribute** with code or documentation

---

<div align="center">

**🚀 Stop manually configuring environments - automate with DevEnv Manager! 🚀**

[🇧🇷 Português](README.pt-br.md) | [🇺🇸 English](README.md)

</div>


