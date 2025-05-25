# 🔥 EnvForge

**Forge, sync and restore complete development environments in minutes**

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Platform](https://img.shields.io/badge/platform-Linux-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Status](https://img.shields.io/badge/status-stable-brightgreen.svg)

---

## 🎯 **What is it?**

EnvForge is a CLI tool that solves one of developers' biggest problems: **reconfiguring development environments from scratch**.

Instead of spending days installing packages, setting up dotfiles and extensions every time you:
- 💻 Get a new laptop
- 🔄 Format your system
- 👥 Need to standardize your team
- 🏠 Want to sync home/work setups

**You simply restore everything automatically with EnvForge!**

---

## 🆚 **EnvForge vs Other Tools**

| | EnvForge | Git/GitHub | Docker | Dotfiles Repos |
|---|---|---|---|---|
| **What it manages** | 🖥️ **Complete environment** | 📝 Source code | 📦 Isolated containers | 📄 Config files only |
| **Installs packages** | ✅ 271 APT packages | ❌ | ❌ | ❌ |
| **System configuration** | ✅ Dotfiles + extensions | ❌ | ❌ | ✅ Configs only |
| **Synchronization** | ✅ Bidirectional Git | ✅ Code only | ❌ | ✅ Configs only |
| **Use case** | 🛠️ Complete personal setup | 📂 Code projects | 🚀 App deployment | ⚙️ Basic configs |

### **Practical Example:**

**❌ Current Situation (2 days of work):**
```bash
# New/reformatted laptop:
sudo apt update && sudo apt install git curl vim...    # 271 packages manually
code --install-extension ms-python.python...          # 15+ VS Code extensions  
cp dotfiles/.bashrc ~/.bashrc                         # Configure terminal
git config --global user.name...                      # Git configs
# ... hundreds of manual steps
```

**✅ With EnvForge (30 minutes):**
```bash
pip install envforge
envforge restore "my-complete-environment"
# ☕ Go grab a coffee - everything automated!
```

---

## 🚀 **Installation**

### **Method 1: Direct Installation (Recommended)**
```bash
# Install via PyPI
pip install envforge
```

### **Method 2: Manual Installation**
```bash
# Clone the repository
git clone https://github.com/bernardoamorimalvarenga/envforge.git
cd envforge

# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -e .

# Test installation
envforge --help
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
# Initialize EnvForge
envforge init

# ✅ Output:
# 🔥 EnvForge initialized successfully!
# Config stored in: /home/user/.envforge
```

### **2. Capture Your Current Environment**

```bash
# Capture everything installed and configured
envforge capture "my-setup-$(date +%Y%m%d)"

# ✅ Example output:
# 🔥 Capturing environment: my-setup-20241201
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
envforge list

# ✅ Example output:
# ┏━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┓
# ┃ Name                 ┃ Created         ┃ File                ┃
# ┡━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━┩
# │ my-setup-20241201    │ 2024-12-01 14:30│ my-setup-20241201.json │
# │ work-environment     │ 2024-11-28 09:15│ work-environment.json  │
# │ complete-setup       │ 2024-11-25 16:45│ complete-setup.json    │
# └──────────────────────┴─────────────────┴─────────────────────────┘
```

### **4. View Environment Details**

```bash
# See what a specific environment contains
envforge show "my-setup-20241201"

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
envforge restore "my-setup-20241201" --dry-run

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
envforge restore "my-setup-20241201"

# ✅ Interactive process:
# 🔥 Restoring environment: my-setup-20241201
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
# Backed up existing .bashrc to .bashrc.envforge-backup
# ✓ Restored .bashrc
# ✓ Restored .vimrc
# 🔌 Installing VS Code extensions...
# ✓ VS Code extensions installed successfully
# ✓ Environment restored successfully!
```

---

## 🔄 **Git Synchronization (Multi-machine)**

### **Initial Setup (Once)**

```bash
# Configure synchronization with private repository
envforge sync setup git@github.com:your-user/envforge-private.git

# ✅ Output:
# 🔧 Setting up git sync with git@github.com:your-user/envforge-private.git
# 
# ╭─ Sync Ready ─╮
# │ Git sync setup complete! │
# │                          │
# │ Repository: git@github.com:your-user/envforge-private.git │
# │ Branch: main             │
# │                          │
# │ Use 'envforge sync push' to upload environments │
# │ Use 'envforge sync pull' to download environments │
# ╰──────────────╯
```

### **Pushing Environments**

```bash
# Send all environments to repository
envforge sync push

# Send only a specific environment
envforge sync push -e "my-setup-20241201"

# Send multiple environments
envforge sync push -e "environment1" -e "environment2"

# ✅ Example output:
# 📤 Pushing specific environments: my-setup-20241201
# ✓ Successfully pushed 1 specific environments
```

### **Downloading Environments**

```bash
# Download environments from repository
envforge sync pull

# ✅ Example output:
# 📥 Pulling environments from remote...
# ✓ Imported work-environment
# ✓ Imported home-setup
# ✓ Successfully imported 2 environments
```

### **Synchronization Status**

```bash
# View sync status
envforge sync status

# ✅ Example output:
# ┏━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃ Property           ┃ Value                                               ┃
# ┡━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
# │ Status             │ ✓ Enabled                                          │
# │ Remote URL         │ git@github.com:your-user/envforge-private.git     │
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
envforge capture "my-complete-setup"
envforge sync push

# On new machine:
pip install envforge
envforge init
envforge sync setup git@github.com:your-user/envforge-private.git
envforge sync pull
envforge restore "my-complete-setup"
# ☕ 30 minutes later: identical environment!
```

### **👥 Case 2: Team Onboarding**
```bash
# Company setup (done once by tech lead):
envforge capture "company-dev-env-2024"  
envforge sync push

# New developer:
envforge sync pull
envforge restore "company-dev-env-2024"
# 🎉 Standardized environment automatically!
```

### **🏠 Case 3: Home/Work Synchronization**
```bash
# At work:
envforge capture "work-setup"
envforge sync push

# At home:
envforge sync pull
envforge restore "work-setup" 
# 🔄 Same environment at home!
```

### **🔄 Case 4: Backup/Disaster Recovery**
```bash
# Regular backup:
envforge capture "backup-$(date +%Y%m%d)"
envforge sync push

# After problem/reformatting:
envforge sync pull
envforge list  # View available backups
envforge restore "backup-20241201"
# 🛡️ Environment restored!
```

---

## 📊 **Available Commands**

### **Basic Commands:**
```bash
envforge init                    # Initialize EnvForge
envforge capture "name"          # Capture current environment
envforge list                    # List saved environments
envforge show "name"             # Show environment details  
envforge restore "name"          # Restore environment
envforge delete "name"           # Delete environment
envforge status                  # Current system status
```

### **Sync Commands:**
```bash
envforge sync setup <repo-url>   # Configure Git synchronization
envforge sync push               # Send all environments
envforge sync push -e "name"     # Send specific environment
envforge sync pull               # Download environments from repository
envforge sync status             # Synchronization status
```

### **Utility Commands:**
```bash
envforge export "name" file.json    # Export to file
envforge import-env file.json       # Import from file
envforge diff "env1" "env2"         # Compare environments
envforge clean                      # Clean old backups
```

### **Useful Options:**
```bash
envforge restore "name" --dry-run     # Preview without applying changes
envforge restore "name" --force       # Skip confirmations
envforge delete "name" --force        # Delete without confirmation
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
    ".bashrc": "# .bashrc content...",
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
- **SSH keys** are not captured by default
- **Automatic backups** of existing files before replacement
- **Dry-run mode** for safe previews
- **Confirmations** before important changes
- **Private repositories** recommended for sync

### **⚠️ Important Considerations:**
- **Use private repositories** for sensitive data
- **Review snapshots** before sharing
- **Dotfiles may contain personal information**
- **Always test with --dry-run** first

### **🛡️ Best Practices:**
```bash
# ✅ Use private repository
envforge sync setup git@github.com:your-user/envforge-PRIVATE.git

# ✅ Always preview first
envforge restore "environment" --dry-run

# ✅ Manual backup before major changes
cp ~/.bashrc ~/.bashrc.backup-$(date +%s)

# ✅ Review what will be installed
envforge show "environment"
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
envforge restore "environment" --force
```

#### **"Git sync failed":**
```bash
# Check if repository is private and you have access
git clone git@github.com:your-user/envforge-private.git

# Reconfigure if necessary
envforge sync setup git@github.com:your-user/envforge-private.git
```

#### **"VS Code extensions failed":**
```bash
# Make sure VS Code is installed
code --version

# Install manually if necessary
envforge show "environment"  # View extension list
```

### **Logs and Debug:**
```bash
# View detailed status
envforge status

# Check config files
ls -la ~/.envforge/

# Preview before applying
envforge restore "environment" --dry-run
```

---

## 🤝 **Contributing**

Contributions are welcome! 

### **How to Contribute:**
1. **Fork** the repository
2. **Create** a branch for your feature (`git checkout -b feature/new-functionality`)
3. **Commit** your changes (`git commit -am 'Add new functionality'`)
4. **Push** to the branch (`git push origin feature/new-functionality`)
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
- [ ] Safe package list (whitelist)
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

**Bernardo**
- GitHub: [@bernardoamorimalvarenga](https://github.com/bernardoamorimalvarenga)
- Email: amorimbernardogame@gmail.com

---

## 🙏 **Acknowledgments**

- **Click** - Fantastic CLI framework
- **Rich** - Beautiful colored interface  
- **Git** - Robust sync system
- **Python Community** - Amazing tools

---

## ⭐ **Like the Project?**

If EnvForge helped you, consider:
- ⭐ **Give it a star** on GitHub
- 🐛 **Report bugs** or **suggest improvements**
- 📢 **Share** with other developers
- 🤝 **Contribute** with code or documentation

---

<div align="center">

**🔥 Stop manually reconfiguring environments - forge with EnvForge! 🔥**

 [🇧🇷 Português](README.pt-br.md) | [🇺🇸 English](README.md)

</div>


