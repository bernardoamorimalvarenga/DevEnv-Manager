"""
Security-related CLI commands for EnvForge
"""

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from ..core.security import security_manager
from ..storage.secure import secure_storage

console = Console()


@click.group()
def security():
    """Security and encryption commands"""
    pass


@security.command()
def status():
    """Show security status of all snapshots"""
    status_info = secure_storage.get_security_status()
    
    # Security overview
    console.print("[bold cyan]🔒 Security Status Overview[/bold cyan]")
    
    overview_table = Table(title="Security Summary")
    overview_table.add_column("Metric", style="cyan")
    overview_table.add_column("Value", style="green")
    
    overview_table.add_row("Total Snapshots", str(status_info["total_snapshots"]))
    overview_table.add_row("Encrypted", str(status_info["encrypted_snapshots"]))
    overview_table.add_row("Integrity Protected", str(status_info["integrity_protected"]))
    
    console.print(overview_table)
    
    # Security configuration
    config_info = status_info["security_config"]
    config_table = Table(title="Security Configuration")
    config_table.add_column("Setting", style="cyan")
    config_table.add_column("Status", style="green")
    
    config_table.add_row("Encryption", "✓ Enabled" if config_info["encryption_enabled"] else "✗ Disabled")
    config_table.add_row("Sensitive Filtering", "✓ Enabled" if config_info["sensitive_filtering"] else "✗ Disabled")
    config_table.add_row("Package Validation", "✓ Enabled" if config_info["package_validation"] else "✗ Disabled")
    
    console.print(config_table)
    
    # Safe packages count
    safe_pkgs = config_info["safe_packages_count"]
    pkg_table = Table(title="Safe Package Whitelist")
    pkg_table.add_column("Package Type", style="cyan")
    pkg_table.add_column("Whitelisted Count", style="green")
    
    for pkg_type, count in safe_pkgs.items():
        pkg_table.add_row(pkg_type.upper(), str(count))
    
    console.print(pkg_table)
    
    # Individual snapshots
    if status_info["snapshots"]:
        snapshots_table = Table(title="Snapshot Security Details")
        snapshots_table.add_column("Name", style="cyan")
        snapshots_table.add_column("Encrypted", style="green")
        snapshots_table.add_column("Integrity", style="yellow")
        snapshots_table.add_column("Created", style="dim")
        
        for snapshot in status_info["snapshots"]:
            encrypted = "🔐 Yes" if snapshot.get("encrypted", False) else "🔓 No"
            integrity = "✓ Protected" if snapshot.get("integrity_protected", False) else "✗ Unprotected"
            created = snapshot.get("created_at", "Unknown")[:19].replace("T", " ")
            
            snapshots_table.add_row(
                snapshot["name"],
                encrypted,
                integrity,
                created
            )
        
        console.print(snapshots_table)


@security.command()
@click.argument("name")
@click.option("--password", "-p", help="Encryption password")
def encrypt(name, password):
    """Encrypt an existing snapshot"""
    console.print(f"[blue]🔐 Encrypting snapshot: {name}[/blue]")
    
    # Load the snapshot
    data = secure_storage.load_snapshot(name, verify_integrity=False)
    if not data:
        console.print(f"[red]❌ Snapshot '{name}' not found![/red]")
        return
    
    # Check if already encrypted
    if data.get("metadata", {}).get("encrypted", False):
        console.print(f"[yellow]⚠️  Snapshot '{name}' is already encrypted![/yellow]")
        return
    
    # Migrate to encrypted format
    if secure_storage.migrate_to_secure(name, encrypt=True, password=password):
        console.print(f"[green]✓ Successfully encrypted snapshot '{name}'[/green]")
    else:
        console.print(f"[red]✗ Failed to encrypt snapshot '{name}'[/red]")


@security.command()
@click.argument("name")
@click.option("--password", "-p", help="Decryption password")
def decrypt(name, password):
    """Decrypt a snapshot (convert to unencrypted format)"""
    console.print(f"[blue]🔓 Decrypting snapshot: {name}[/blue]")
    
    # Load the encrypted snapshot
    data = secure_storage.load_snapshot(name, password=password)
    if not data:
        console.print(f"[red]❌ Could not load or decrypt snapshot '{name}'![/red]")
        return
    
    # Check if it's encrypted
    if not data.get("metadata", {}).get("encrypted", False):
        console.print(f"[yellow]⚠️  Snapshot '{name}' is not encrypted![/yellow]")
        return
    
    # Save as unencrypted
    if secure_storage.migrate_to_secure(name, encrypt=False):
        console.print(f"[green]✓ Successfully decrypted snapshot '{name}'[/green]")
    else:
        console.print(f"[red]✗ Failed to decrypt snapshot '{name}'[/red]")


@security.command()
@click.argument("name")
@click.option("--password", "-p", help="Password for encrypted snapshots")
def verify(name, password):
    """Verify integrity of a snapshot"""
    console.print(f"[blue]🔍 Verifying integrity of: {name}[/blue]")
    
    # Attempt to load with integrity verification
    data = secure_storage.load_snapshot(name, password=password, verify_integrity=True)
    
    if data:
        console.print(f"[green]✓ Snapshot '{name}' passed integrity verification[/green]")
        
        # Show security details if available
        if "security" in data:
            security_info = data["security"]
            
            details_table = Table(title="Security Details")
            details_table.add_column("Feature", style="cyan")
            details_table.add_column("Status", style="green")
            
            details_table.add_row("Encryption", "✓ Yes" if security_info["encryption_enabled"] else "✗ No")
            details_table.add_row("Sensitive Filtering", "✓ Yes" if security_info["sensitive_filtering"] else "✗ No")
            details_table.add_row("Package Validation", "✓ Yes" if security_info["package_validation"] else "✗ No")
            
            if security_info.get("package_report"):
                pkg_report = security_info["package_report"]
                details_table.add_row("Packages Blocked", str(pkg_report.get("blocked_count", 0)))
                details_table.add_row("Total Packages", str(pkg_report.get("total_count", 0)))
            
            console.print(details_table)
            
            # Show warnings if any
            if security_info.get("warnings"):
                console.print("[yellow]⚠️  Security Warnings:[/yellow]")
                for warning in security_info["warnings"]:
                    console.print(f"  • {warning}")
    else:
        console.print(f"[red]✗ Snapshot '{name}' failed verification or could not be loaded[/red]")


@security.command()
def packages():
    """Manage safe package whitelist"""
    safe_packages = security_manager.safe_packages
    
    console.print("[bold cyan]📦 Safe Package Whitelist[/bold cyan]")
    
    for pkg_type, pkg_set in safe_packages.items():
        if pkg_set:
            console.print(f"\n[bold]{pkg_type.upper()}[/bold] ({len(pkg_set)} packages)")
            
            # Show first 10 packages per type
            pkg_list = sorted(list(pkg_set))
            for i, pkg in enumerate(pkg_list[:10]):
                console.print(f"  • {pkg}")
            
            if len(pkg_list) > 10:
                console.print(f"  ... and {len(pkg_list) - 10} more")


@security.command()
@click.argument("package_type", type=click.Choice(["apt", "snap", "flatpak", "pip"]))
@click.argument("packages", nargs=-1, required=True)
@click.option("--remove", is_flag=True, help="Remove packages from whitelist")
def whitelist(package_type, packages, remove):
    """Add or remove packages from the safe whitelist"""
    action = "remove" if remove else "add"
    
    if security_manager.update_safe_packages(package_type, list(packages), action):
        verb = "removed from" if remove else "added to"
        console.print(f"[green]✓ {len(packages)} packages {verb} {package_type} whitelist[/green]")
        
        # Show updated count
        count = len(security_manager.safe_packages[package_type])
        console.print(f"[dim]Total {package_type} packages in whitelist: {count}[/dim]")
    else:
        console.print(f"[red]✗ Failed to update whitelist[/red]")


@security.command()
@click.argument("name")
@click.option("--show-blocked", is_flag=True, help="Show blocked packages")
def scan(name, show_blocked):
    """Scan a snapshot for security issues"""
    console.print(f"[blue]🔍 Scanning snapshot for security issues: {name}[/blue]")
    
    # Load snapshot
    data = secure_storage.load_snapshot(name, verify_integrity=False)
    if not data:
        console.print(f"[red]❌ Snapshot '{name}' not found![/red]")
        return
    
    issues = []
    
    # Check if encrypted
    is_encrypted = data.get("metadata", {}).get("encrypted", False)
    if not is_encrypted:
        issues.append("Snapshot is not encrypted")
    
    # Check packages
    if "packages" in data:
        pkg_report = security_manager.validate_packages(data["packages"])
        
        if pkg_report["blocked_count"] > 0:
            issues.append(f"{pkg_report['blocked_count']} unsafe packages detected")
            
            if show_blocked:
                console.print("\n[yellow]🚫 Blocked Packages:[/yellow]")
                for pkg_type, pkgs in pkg_report["unsafe_packages"].items():
                    if pkgs:
                        console.print(f"  {pkg_type.upper()}:")
                        for pkg in pkgs[:5]:  # Show first 5
                            console.print(f"    • {pkg}")
                        if len(pkgs) > 5:
                            console.print(f"    ... and {len(pkgs) - 5} more")
    
    # Check dotfiles for sensitive data
    if "dotfiles" in data:
        sensitive_files = []
        for filename, content in data["dotfiles"].items():
            _, warnings = security_manager.filter_sensitive_data(content, filename)
            if warnings:
                sensitive_files.append(filename)
        
        if sensitive_files:
            issues.append(f"Sensitive data detected in {len(sensitive_files)} dotfiles")
    
    # Display results
    if issues:
        console.print(f"\n[red]❌ {len(issues)} security issues found:[/red]")
        for issue in issues:
            console.print(f"  • {issue}")
    else:
        console.print(f"\n[green]✓ No security issues found in '{name}'[/green]")


@security.command()
@click.option("--encryption/--no-encryption", default=True, help="Enable encryption by default")
@click.option("--filtering/--no-filtering", default=True, help="Enable sensitive data filtering")
@click.option("--validation/--no-validation", default=True, help="Enable package validation")
def configure(encryption, filtering, validation):
    """Configure security settings"""
    from ..core.config import config
    
    # Update config
    security_config = {
        "encryption": encryption,
        "filter_sensitive": filtering,
        "validate_packages": validation
    }
    
    config.settings.setdefault("security", {}).update(security_config)
    config.save_config()
    
    console.print("[green]✓ Security configuration updated:[/green]")
    console.print(f"  • Encryption: {'✓ Enabled' if encryption else '✗ Disabled'}")
    console.print(f"  • Sensitive Filtering: {'✓ Enabled' if filtering else '✗ Disabled'}")
    console.print(f"  • Package Validation: {'✓ Enabled' if validation else '✗ Disabled'}")