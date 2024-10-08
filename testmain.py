import os
import json
import sys
from rich.console import Console
from contextlib import redirect_stdout, redirect_stderr
from fpdf import FPDF

# Importing functions from source directories
from source.ui.banner import banner
from source.operations.decompile_apk import decompile_apk
from source.operations.recompile_apk import recompile_apk
from source.operations.modify_code import modify_code
from source.operations.screenshot import take_screenshot
from source.operations.sign_apk import sign_apk

# Importing functions from APK_INFO directories
from source.APK_INFO.apk_activities import get_apk_activities
from source.APK_INFO.apk_info import get_apk_info
from source.APK_INFO.apk_permissions import get_apk_permissions
from source.APK_INFO.apk_services import get_apk_services

# Initialize console for rich output
console = Console()

# Base directory for reports
report_base_dir = os.path.join(os.getcwd(), 'Report')

# Create report directory if it doesn't exist
if not os.path.exists(report_base_dir):
    os.makedirs(report_base_dir)

# Words to search in APK before modification
search_words_before_modification = [
    'android:debuggable="true"', 'android:allowBackup="true"', 'android:usesCleartextTrafic="true"', 
    'android:exported="true"', '.setJavaScriptEnabled(true)', '"google_api_key"', 
    '"Google_Api_Key"', '"google_crash_reporting_api_key"', 
    'websettings.setAllowFileAccess(true)', 'setPluginState()', '.firebaseio.com'
]

# Generate PDF report from the log file
def generate_pdf_report(log_file_path):
    try:
        # Initialize PDF object
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()

        # Set title and header
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(200, 10, txt="APK Process Report", ln=True, align='C')

        # Set font for content
        pdf.set_font('Arial', '', 12)

        # Read the log file and write its content to the PDF
        if os.path.exists(log_file_path):
            with open(log_file_path, 'r', encoding='utf-8') as log_file:  # Use 'utf-8' encoding
                for line in log_file:
                    # Handle encoding errors gracefully by replacing unsupported characters
                    sanitized_line = line.encode('latin-1', 'replace').decode('latin-1')
                    pdf.multi_cell(0, 10, sanitized_line)
        else:
            console.print(f"[red][!][/red] [bold red]Error:[/bold red] Log file not found!")

        # Save the PDF
        pdf_output_path = os.path.join(report_base_dir, 'apk_process_report.pdf')
        pdf.output(pdf_output_path)

        console.print(f"[green][+][/green] [bold green]PDF report saved as:[/bold green] {pdf_output_path}")
    
    except Exception as e:
        console.print(f"[red][!][/red] [bold red]Failed to generate PDF report:[/bold red] {e}")


# Tee class for sending output to both the console and the log file
class Tee:
    def __init__(self, log_file, console):
        self.log_file = log_file
        self.console = console

    def write(self, data):
        self.log_file.write(data)
        self.console.write(data)

    def flush(self):
        self.log_file.flush()
        self.console.flush()

# Collect APK information
def collect_apk_info(apk_path):
    get_apk_info(apk_path)
    get_apk_activities(apk_path)
    get_apk_permissions(apk_path)
    get_apk_services(apk_path)
    console.print("\n")


def main():
    log_file_path = os.path.join(report_base_dir, 'apk_process_log.txt')

    # Open the log file
    with open(log_file_path, 'w', encoding='utf-8') as log_file:  # Use 'utf-8' encoding for the log file
        # Create a Tee object that writes to both the console and the log file
        tee_stdout = Tee(log_file, sys.stdout)
        tee_stderr = Tee(log_file, sys.stderr)

        # Redirect stdout and stderr to both the log file and console
        with redirect_stdout(tee_stdout), redirect_stderr(tee_stderr):
            # Load tool paths from configuration file
            try:
                with open('tools_config.json', 'r') as config_file:
                    config = json.load(config_file)
            except FileNotFoundError:
                console.print("[red][!][/red] [bold red]Error:[/bold red] tools_config.json file not found!")
                sys.exit(1)

            banner()

            # Check if APK path is provided as a command-line argument
            if len(sys.argv) < 2:
                console.print("[red][-][/red] [bold red]Error:[/bold red] APK path is required!", style="bold red")
                sys.exit(1)

            apk_path = sys.argv[1]
            apk_name = os.path.splitext(os.path.basename(apk_path))[0]
            output_dir = os.path.join(report_base_dir, apk_name)

            # Collect APK Info
            console.print("[cyan][+][/cyan][bold cyan] Collecting APK info ...[/bold cyan]")
            collect_apk_info(apk_path)

            # Decompile APK
            console.print("[cyan][+][/cyan][bold cyan] Decompiling APK...[/bold cyan]")
            decompile_img_path = os.path.join(report_base_dir, 'decompile.png')
            decompile_apk(apk_path, output_dir, decompile_img_path)


            # Recompile the APK
            console.print("[cyan][+][/cyan][bold cyan] Recompiling APK ...[/bold cyan]")
            recompile_apk_path = os.path.join(report_base_dir, f"new_{apk_name}.apk")
            recompile_apk(output_dir, recompile_apk_path)
            console.print("\n" * 1)

            # Signing the recompiled APK
            console.print("[cyan][+][/cyan][bold cyan] Signing APK ...[/bold cyan]")
            sig_key_path = os.path.join(os.getcwd(), 'sign_key.jks')
            sign_apk(recompile_apk_path, sig_key_path, 'root_alias', 'root@123')

            console.print("\n" * 1)
            console.print("[green][+][/green] [bold green]Process completed successfully![/bold green]")

    # After finishing the console output capture, generate the PDF report
    generate_pdf_report(log_file_path)


# Run the main function
if __name__ == "__main__":
    main()
