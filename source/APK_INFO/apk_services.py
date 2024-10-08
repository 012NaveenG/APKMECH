from androguard.core.bytecodes.apk import APK
from rich.console import Console
from rich.table import Table

def get_apk_services(apk_path):
    # Initialize Rich Console
    console = Console()

    # Load the APK
    apk = APK(apk_path)

    # Retrieve services
    services = apk.get_services()

    # Create a Rich table for services
    table = Table(title="[green]APK Services[/green]", show_header=True, header_style="bold magenta")
    table.add_column("Sr. No.", style="cyan")
    table.add_column("Service", style="cyan")

    # Add rows to the table for each service with serial numbers
    for idx, service in enumerate(services, start=1):
        table.add_row(f"{idx}", service)

    # Print the table using Rich
    console.print(table)
