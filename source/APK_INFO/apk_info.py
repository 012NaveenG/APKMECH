from androguard.core.bytecodes.apk import APK
from rich.console import Console
from rich.table import Table

def get_apk_info(apk_path):
    # Initialize Rich Console
    console = Console()

    # Load the APK
    apk = APK(apk_path)

    # Check if the APK is signed and retrieve signature information
    signatures = apk.get_signature_names()
    is_signed = "True" if signatures else "False"

    # Placeholder for signature versions
    signature_v1 = "True" if 'v1' in signatures else "False"
    signature_v2 = "True" if 'v2' in signatures else "False"
    signature_v3 = "True" if 'v3' in signatures else "False"

    # Create a Rich table for APK info
    table = Table(title="[green]APK Standard Information[/green]", show_header=False)
    # Add rows to the table for each APK detail
    table.add_row("[green]Package Name:[/green]", apk.get_package())
    table.add_row("[green]App Name:[/green]", apk.get_app_name())
    table.add_row("[green]Is App Signed:[/green]", is_signed)

    # Nested table for signature versions
    sig_table = Table(show_header=False, box=None)
    sig_table.add_row("[blue]Signature Version 1:[/blue]", signature_v1)
    sig_table.add_row("[blue]Signature Version 2:[/blue]", signature_v2)
    sig_table.add_row("[blue]Signature Version 3:[/blue]", signature_v3)

    # Add the nested signature version table to the main table
    table.add_row("[green]Signature Versions:[/green]", sig_table)

    # Add row for package signature file
    table.add_row("[green]Package Signature:[/green]", signatures[0] if signatures else 'No Signature Found')

    # Print the table using Rich
    console.print(table)
