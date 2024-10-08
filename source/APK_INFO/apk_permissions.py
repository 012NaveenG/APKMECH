from androguard.core.bytecodes.apk import APK
from rich.console import Console
from rich.table import Table

def get_apk_permissions(apk_path):
    # Initialize Rich Console
    console = Console()

    # Load the APK
    apk = APK(apk_path)

    # Retrieve permissions
    permissions = apk.get_permissions()

    # Create a Rich table for permissions
    table = Table(title="[green]APK Permissions[/green]", show_header=True, header_style="bold magenta")
    table.add_column("Sr. No.", style="cyan")
    table.add_column("Permission", style="cyan")

    # Add rows to the table for each permission with serial numbers
    for idx, permission in enumerate(permissions, start=1):
        table.add_row(f"{idx}", permission)

    # Print the table using Rich
    console.print(table)
