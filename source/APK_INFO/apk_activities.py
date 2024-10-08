from androguard.core.bytecodes.apk import APK
from rich.console import Console
from rich.table import Table

def get_apk_activities(apk_path):
    # Initialize Rich Console
    console = Console()

    # Load the APK
    apk = APK(apk_path)

    # Retrieve activities
    activities = apk.get_activities()

    # Create a Rich table for activities
    table = Table(title="[green]APK Activities[/green]", show_header=True, header_style="bold magenta")
    table.add_column("Sr. No.", style="cyan")
    table.add_column("Activity", style="cyan")

    # Add rows to the table for each activity with serial numbers
    for idx, activity in enumerate(activities, start=1):
        table.add_row(f"{idx}", activity)

    # Print the table using Rich
    console.print(table)
