from setuptools import setup, find_packages

setup(
    name="devenv-manager",
    version="0.1.0",
    description="Development Environment Manager for Linux",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "click>=8.0.0",
        "rich>=13.0.0",
        "pyyaml>=6.0",
        "gitpython>=3.1.0",
        "psutil>=5.9.0",
    ],
    entry_points={
        "console_scripts": [
            "devenv=devenv.cli.main:cli",
        ],
    },
    python_requires=">=3.8",
)
