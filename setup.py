from setuptools import setup, find_packages

# Ler README com encoding UTF-8 para evitar problemas
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="devenv-manager",
    version="0.1.2",
    description="Development Environment Manager for Linux - Backup, sync and restore your dev environment in minutes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Bernardo Amorim Alvarenga",
    author_email="amorimbernardogame@gmail.com",
    url="https://github.com/bernardoamorimalvarenga/devenv-manager",
    
    # Links importantes que aparecem no PyPI
    project_urls={
        "Bug Reports": "https://github.com/bernardoamorimalvarenga/devenv-manager/issues",
        "Source": "https://github.com/bernardoamorimalvarenga/devenv-manager",
        "Documentation": "https://github.com/bernardoamorimalvarenga/devenv-manager#readme",
        "Changelog": "https://github.com/bernardoamorimalvarenga/devenv-manager/blob/main/CHANGELOG.md",
    },
    
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    
    install_requires=[
        "click>=8.0.0",
        "rich>=13.0.0",
        "pyyaml>=6.0",
        "gitpython>=3.1.0",
        "psutil>=5.9.0",
    ],
    
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "flake8>=6.0.0",
            "autoflake>=2.0.0",
        ]
    },
    
    entry_points={
        "console_scripts": [
            "devm=devenv.cli.main:cli",
        ],
    },
    
    python_requires=">=3.8",
    
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Systems Administration",
        "Topic :: System :: Archiving :: Backup",
        "Topic :: Utilities",
        "Environment :: Console",
    ],
    
    keywords="linux development environment backup sync cli devops dotfiles packages git automation",
    
    # Metadados adicionais para melhor descoberta
    platforms=["Linux"],
    zip_safe=False,
)
