# 🔥 EnvForge

**Forje, sincronize e restaure ambientes de desenvolvimento completos em minutos**

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Platform](https://img.shields.io/badge/platform-Linux-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Status](https://img.shields.io/badge/status-stable-brightgreen.svg)

---

## 🎯 **O Que É?**

O EnvForge é uma ferramenta CLI que resolve um dos maiores problemas dos desenvolvedores: **reconfigurar ambientes de desenvolvimento do zero**.

Em vez de passar dias instalando pacotes, configurando dotfiles e extensões toda vez que você:
- 💻 Compra um laptop novo
- 🔄 Formata o sistema  
- 👥 Precisa padronizar a equipe
- 🏠 Quer sincronizar casa/trabalho

**Você simplesmente restaura tudo automaticamente com EnvForge!**

---

## 🆚 **EnvForge vs Outras Ferramentas**

| | EnvForge | Git/GitHub | Docker | Dotfiles Repos |
|---|---|---|---|---|
| **O que gerencia** | 🖥️ **Ambiente completo** | 📝 Código fonte | 📦 Containers isolados | 📄 Apenas configs |
| **Instala pacotes** | ✅ 271 pacotes APT | ❌ | ❌ | ❌ |
| **Configura sistema** | ✅ Dotfiles + extensões | ❌ | ❌ | ✅ Só configs |
| **Sincronização** | ✅ Git bidirecional | ✅ Código apenas | ❌ | ✅ Configs apenas |
| **Caso de uso** | 🛠️ Setup pessoal completo | 📂 Projetos de código | 🚀 Deploy apps | ⚙️ Configs básicas |

### **Exemplo Prático:**

**❌ Situação Atual (2 dias de trabalho):**
```bash
# Laptop novo/formatado:
sudo apt update && sudo apt install git curl vim...    # 271 pacotes manualmente
code --install-extension ms-python.python...          # 15+ extensões VS Code  
cp dotfiles/.bashrc ~/.bashrc                         # Configurar terminal
git config --global user.name...                      # Git configs
# ... centenas de passos manuais
```

**✅ Com EnvForge (30 minutos):**
```bash
pip install envforge
envforge restore "meu-ambiente-completo"
# ☕ Vai tomar um café - tudo automatizado!
```

---

## 🚀 **Instalação**

### **Método 1: Instalação Direta (Recomendado)**
```bash
# Instalar via PyPI
pip install envforge
```

### **Método 2: Instalação Manual**
```bash
# Clone o repositório
git clone https://github.com/bernardoamorimalvarenga/envforge.git
cd envforge

# Crie ambiente virtual
python -m venv .venv
source .venv/bin/activate

# Instale as dependências
pip install -e .

# Teste a instalação
envforge --help
```

### **Requisitos do Sistema:**
- 🐧 **Linux** (Ubuntu 20.04+, Debian 10+, Arch, Fedora)
- 🐍 **Python 3.8+**
- 🔑 **sudo** (para instalação de pacotes)
- 📦 **git** (para sincronização)

---

## 📋 **Guia de Uso Completo**

### **1. Primeira Configuração**

```bash
# Inicialize o EnvForge
envforge init

# ✅ Saída:
# 🔥 EnvForge initialized successfully!
# Config stored in: /home/usuario/.envforge
```

### **2. Capturar Seu Ambiente Atual**

```bash
# Capture tudo que está instalado e configurado
envforge capture "meu-setup-$(date +%Y%m%d)"

# ✅ Saída exemplo:
# 🔥 Capturing environment: meu-setup-20241201
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
# ✓ Environment 'meu-setup-20241201' captured successfully!
```

### **3. Ver Ambientes Salvos**

```bash
# Liste todos os ambientes capturados
envforge list

# ✅ Saída exemplo:
# ┏━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┓
# ┃ Name                 ┃ Created         ┃ File                ┃
# ┡━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━┩
# │ meu-setup-20241201   │ 2024-12-01 14:30│ meu-setup-20241201.json │
# │ ambiente-trabalho    │ 2024-11-28 09:15│ ambiente-trabalho.json  │
# │ setup-completo       │ 2024-11-25 16:45│ setup-completo.json     │
# └──────────────────────┴─────────────────┴─────────────────────────┘
```

### **4. Ver Detalhes de um Ambiente**

```bash
# Veja o que contém um ambiente específico
envforge show "meu-setup-20241201"

# ✅ Saída exemplo:
# 📋 Environment Details: meu-setup-20241201
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

### **5. Restaurar um Ambiente**

#### **Preview Seguro (Dry Run):**
```bash
# Veja o que será feito SEM aplicar mudanças
envforge restore "meu-setup-20241201" --dry-run

# ✅ Saída exemplo:
# 🔍 DRY RUN MODE - No changes will be made
# 📦 Restoring packages...
# Would install 45 new APT packages
# Would install: git vim curl nodejs python3-pip code...
# 📝 Would restore 8 dotfiles
# 🔌 Would install 12 new VS Code extensions
# ✓ Dry run completed successfully!
```

#### **Restauração Real:**
```bash
# Restaure o ambiente (VAI INSTALAR OS PACOTES)
envforge restore "meu-setup-20241201"

# ✅ Processo interativo:
# 🔥 Restoring environment: meu-setup-20241201
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

## 🔄 **Sincronização Git (Multi-máquina)**

### **Setup Inicial (Uma vez)**

```bash
# Configure sincronização com repositório privado
envforge sync setup git@github.com:seu-usuario/envforge-private.git

# ✅ Saída:
# 🔧 Setting up git sync with git@github.com:seu-usuario/envforge-private.git
# 
# ╭─ Sync Ready ─╮
# │ Git sync setup complete! │
# │                          │
# │ Repository: git@github.com:seu-usuario/envforge-private.git │
# │ Branch: main             │
# │                          │
# │ Use 'envforge sync push' to upload environments │
# │ Use 'envforge sync pull' to download environments │
# ╰──────────────╯
```

### **Enviando Ambientes**

```bash
# Envie todos os ambientes para o repositório
envforge sync push

# Envie apenas um ambiente específico
envforge sync push -e "meu-setup-20241201"

# Envie múltiplos ambientes
envforge sync push -e "ambiente1" -e "ambiente2"

# ✅ Saída exemplo:
# 📤 Pushing specific environments: meu-setup-20241201
# ✓ Successfully pushed 1 specific environments
```

### **Baixando Ambientes**

```bash
# Baixe ambientes do repositório
envforge sync pull

# ✅ Saída exemplo:
# 📥 Pulling environments from remote...
# ✓ Imported ambiente-trabalho
# ✓ Imported setup-casa
# ✓ Successfully imported 2 environments
```

### **Status da Sincronização**

```bash
# Veja status do sync
envforge sync status

# ✅ Saída exemplo:
# ┏━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃ Property           ┃ Value                                               ┃
# ┡━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
# │ Status             │ ✓ Enabled                                          │
# │ Remote URL         │ git@github.com:seu-usuario/envforge-private.git   │
# │ Branch             │ main                                               │
# │ Uncommitted Changes │ No                                                │
# │ Last Commit        │ abc123 - Sync 2 environments                      │
# └────────────────────┴────────────────────────────────────────────────────┘
```

---

## 💼 **Casos de Uso Práticos**

### **🆕 Caso 1: Laptop Novo**
```bash
# Na máquina antiga:
envforge capture "meu-setup-completo"
envforge sync push

# Na máquina nova:
pip install envforge
envforge init
envforge sync setup git@github.com:seu-usuario/envforge-private.git
envforge sync pull
envforge restore "meu-setup-completo"
# ☕ 30 minutos depois: ambiente idêntico!
```

### **👥 Caso 2: Onboarding de Equipe**
```bash
# Setup da empresa (feito uma vez pelo tech lead):
envforge capture "empresa-dev-env-2024"  
envforge sync push

# Novo desenvolvedor:
envforge sync pull
envforge restore "empresa-dev-env-2024"
# 🎉 Ambiente padronizado automaticamente!
```

### **🏠 Caso 3: Sincronização Casa/Trabalho**
```bash
# No trabalho:
envforge capture "work-setup"
envforge sync push

# Em casa:
envforge sync pull
envforge restore "work-setup" 
# 🔄 Mesmo ambiente em casa!
```

### **🔄 Caso 4: Backup/Disaster Recovery**
```bash
# Backup regular:
envforge capture "backup-$(date +%Y%m%d)"
envforge sync push

# Depois de problema/formatação:
envforge sync pull
envforge list  # Ver backups disponíveis
envforge restore "backup-20241201"
# 🛡️ Ambiente restaurado!
```

---

## 📊 **Comandos Disponíveis**

### **Comandos Básicos:**
```bash
envforge init                    # Inicializar EnvForge
envforge capture "nome"          # Capturar ambiente atual
envforge list                    # Listar ambientes salvos
envforge show "nome"             # Mostrar detalhes do ambiente  
envforge restore "nome"          # Restaurar ambiente
envforge delete "nome"           # Deletar ambiente
envforge status                  # Status do sistema atual
```

### **Comandos de Sync:**
```bash
envforge sync setup <repo-url>   # Configurar sincronização Git
envforge sync push               # Enviar todos os ambientes
envforge sync push -e "nome"     # Enviar ambiente específico
envforge sync pull               # Baixar ambientes do repositório
envforge sync status             # Status da sincronização
```

### **Comandos Utilitários:**
```bash
envforge export "nome" arquivo.json    # Exportar para arquivo
envforge import-env arquivo.json       # Importar de arquivo
envforge diff "env1" "env2"           # Comparar ambientes
envforge clean                        # Limpar backups antigos
```

### **Opções Úteis:**
```bash
envforge restore "nome" --dry-run     # Preview sem aplicar mudanças
envforge restore "nome" --force       # Pular confirmações
envforge delete "nome" --force        # Deletar sem confirmação
```

---

## 🎯 **O Que É Capturado**

### **📦 Pacotes do Sistema:**
- **APT packages** (apenas manually installed)
- **Snap packages** 
- **Flatpak packages**
- **PIP packages** (globais)

### **⚙️ Configurações:**
- **Dotfiles importantes**: `.bashrc`, `.bash_profile`, `.zshrc`, `.profile`
- **Configs de ferramentas**: `.vimrc`, `.gitconfig`
- **SSH config**: `.ssh/config` (opcional, desabilitado por padrão)

### **🔌 Extensões e Tools:**
- **VS Code**: Todas as extensões instaladas
- **System info**: OS, kernel, arquitetura, Python version

### **Exemplo de Snapshot (JSON):**
```json
{
  "metadata": {
    "name": "meu-setup-20241201",
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
    ".bashrc": "# Conteúdo do .bashrc...",
    ".vimrc": "# Configurações do Vim..."
  },
  "vscode_extensions": [
    "ms-python.python",
    "ms-vscode.vscode-json"
  ]
}
```

---

## 🔒 **Segurança**

### **✅ Configurações Seguras:**
- **SSH keys** não são capturadas por padrão
- **Backups automáticos** de arquivos existentes antes de substituir
- **Dry-run mode** para preview seguro
- **Confirmações** antes de mudanças importantes
- **Repositórios privados** recomendados para sync

### **⚠️ Cuidados Importantes:**
- **Use repositórios privados** para dados sensíveis
- **Revise snapshots** antes de compartilhar
- **Dotfiles podem conter informações pessoais**
- **Sempre teste com --dry-run** primeiro

### **🛡️ Boas Práticas:**
```bash
# ✅ Use repositório privado
envforge sync setup git@github.com:seu-usuario/envforge-PRIVATE.git

# ✅ Sempre faça preview primeiro
envforge restore "ambiente" --dry-run

# ✅ Backup manual antes de grandes mudanças
cp ~/.bashrc ~/.bashrc.backup-$(date +%s)

# ✅ Revise o que será instalado
envforge show "ambiente"
```

---

## 🚀 **Performance**

### **Tempos Típicos:**
- **Captura**: ~30 segundos (271 pacotes + configs)
- **Restore APT**: ~15 minutos (271 pacotes)
- **Restore Snap**: ~5 minutos (26 pacotes)
- **Dotfiles**: ~1 segundo
- **VS Code extensions**: ~2 minutos

### **Tamanhos:**
- **Snapshot JSON**: ~16KB por ambiente
- **Repositório sync**: ~1MB (10 ambientes)

---

## 🐛 **Troubleshooting**

### **Problemas Comuns:**

#### **"Permission denied" durante restore:**
```bash
# Certifique-se que tem sudo
sudo echo "teste"

# Execute com confirmação
envforge restore "ambiente" --force
```

#### **"Git sync failed":**
```bash
# Verifique se o repositório é privado e você tem acesso
git clone git@github.com:seu-usuario/envforge-private.git

# Reconfigure se necessário
envforge sync setup git@github.com:seu-usuario/envforge-private.git
```

#### **"VS Code extensions failed":**
```bash
# Certifique-se que VS Code está instalado
code --version

# Instale manualmente se necessário
envforge show "ambiente"  # Ver lista de extensões
```

### **Logs e Debug:**
```bash
# Ver status detalhado
envforge status

# Verificar arquivos de config
ls -la ~/.envforge/

# Preview antes de aplicar
envforge restore "ambiente" --dry-run
```

---

## 🤝 **Contribuindo**

Contribuições são bem-vindas! 

### **Como Contribuir:**
1. **Fork** o repositório
2. **Crie** uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. **Commit** suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. **Push** para a branch (`git push origin feature/nova-funcionalidade`)
5. **Abra** um Pull Request

### **Áreas que Precisam de Ajuda:**
- **Suporte a outras distros** (CentOS, OpenSUSE)
- **Package managers adicionais** (brew, chocolatey)
- **Testes automatizados**
- **Documentação**
- **Interface gráfica**

---

## 🗺️ **Roadmap**

### **v0.2.0 - Segurança** (Próximas 4 semanas)
- [ ] Encriptação de snapshots
- [ ] Lista de pacotes seguros (whitelist)
- [ ] Filtro de dados sensíveis
- [ ] Verificação de integridade

### **v0.3.0 - Multi-OS** (8 semanas)
- [ ] Suporte Windows (WSL)
- [ ] Suporte macOS
- [ ] Homebrew support
- [ ] Chocolatey support

### **v1.0.0 - GUI e Cloud** (12 semanas)
- [ ] Interface gráfica (PyQt6)
- [ ] Cloud storage (Google Drive, Dropbox)
- [ ] Templates da comunidade
- [ ] Versão Pro com recursos avançados

---

## 📄 **Licença**

Este projeto está licenciado sob a MIT License - veja o arquivo [LICENSE](LICENSE) para detalhes.

---

## 👨‍💻 **Autor**

**Bernardo**
- GitHub: [@bernardoamorimalvarenga](https://github.com/bernardoamorimalvarenga)
- Email: amorimbernardogame@gmail.com

---

## 🙏 **Agradecimentos**

- **Click** - Framework CLI fantástico
- **Rich** - Interface colorida e bonita  
- **Git** - Sistema de sync robusto
- **Comunidade Python** - Ferramentas incríveis

---

## ⭐ **Gostou do Projeto?**

Se o EnvForge te ajudou, considere:
- ⭐ **Dar uma estrela** no GitHub
- 🐛 **Reportar bugs** ou **sugerir melhorias**
- 📢 **Compartilhar** com outros desenvolvedores
- 🤝 **Contribuir** com código ou documentação

---

<div align="center">

**🔥 Pare de reconfigurar ambientes manualmente - forje com EnvForge! 🔥**

 [🇧🇷 Português](README.pt-br.md) | [🇺🇸 English](README.md)

</div>

