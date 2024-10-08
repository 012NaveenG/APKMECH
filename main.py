import os
import json
import sys
from rich.console import Console

# Importing  functions from source directories
from source.ui.banner import banner
from source.operations.decompile_apk import decompile_apk
from source.operations.recompile_apk import recompile_apk
from source.operations.modify_code import modify_code
from source.operations.screenshot import take_screenshot
from source.operations.sign_apk import sign_apk

#iporting functions from APK_INFO directories
from source.APK_INFO.apk_activities import get_apk_activities
from source.APK_INFO.apk_info import get_apk_info
from source.APK_INFO.apk_permissions import get_apk_permissions
from source.APK_INFO.apk_services import get_apk_services

# Initialize console for rich output
console = Console()

report_base_dir = os.path.join(os.getcwd(),'Report')

search_words_before_modification = [
        'android:debuggable="true"', 'android:allowBackup="true"', 'android:usesCleartextTrafic="true"', 
        'android:exported="true"', '.setJavaScriptEnabled(true)', '"google_api_key"', 
        '"Google_Api_Key"', '"google_crash_reporting_api_key"', 
        'websettings.setAllowFileAccess(true)', 'setPluginState()', '.firebaseio.com'
    ]

def collect_apk_info(apk_path):
    get_apk_info(apk_path)
    get_apk_activities(apk_path)
    get_apk_permissions(apk_path)
    get_apk_services(apk_path)
    console.print("\n" * 1)



def searching_the_secret_word(root_directory, screenshot_dir, search_words):
    found_any = False  # Flag to track if any word has been found
    found_words = []  # List to store found words
    for dirpath, _, filenames in os.walk(root_directory):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            
            # Skip files with a .smali extension
            if filename.endswith('.smali'):
                continue
            
            with open(filepath, "r", encoding="utf-8", errors="replace") as file:
                for line_number, line in enumerate(file, start=1):
                    for search_word in search_words:
                        if search_word in line:
                            if not found_any:  # Print scanning message only once
                                found_any = True
                            take_screenshot(filepath, screenshot_dir, line_number, search_word)
                            found_words.append((search_word, filepath, line_number))  # Store found word with filepath and line number
                            
    return found_any, found_words

def modify_secret_word(root_directory, search_words):
    for dirpath, _, filenames in os.walk(root_directory):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            with open(filepath, "r", encoding="utf-8", errors="replace") as file:
                for _, line in enumerate(file, start=1):
                    for search_word in search_words:
                        if search_word in line:
                            modify_code(filepath)

def main():
    # Load tool paths from configuration file
    with console.status("[bold green]Loading tool configuration...[/bold green]") as status:
        try:
            with open('tools_config.json', 'r') as config_file:
                config = json.load(config_file)
        except FileNotFoundError:
            console.print("[red][!][/red] [bold red]Error:[/bold red] [bold red]tools_config.json file not found![/bold red]")
            sys.exit(1)

    banner()

    if len(sys.argv) < 2:
        console.print("[red][-][/red] [bold red]Error:[/bold red] APK path is required!", style="bold red")
        sys.exit(1)

    apk_path = sys.argv[1]
    apk_name = os.path.splitext(os.path.basename(apk_path))[0]
    output_dir = os.path.join(report_base_dir, apk_name)

    # Collect APK Info
    console.print("[cyan][+][/cyan][bold cyan] Collecting APK info ...[/bold cyan]")
    collect_apk_info(apk_path)
    console.print("\n" * 1)

    # Decompile APK
    console.print("[cyan][+][/cyan][bold cyan] Decompiling APK...[/bold cyan]")
    decompile_img_path = os.path.join(report_base_dir,'decompile.png')
    decompile_apk(apk_path, output_dir, decompile_img_path)

    root_directory = os.path.join(output_dir)
    screenshot_dir = os.path.join(report_base_dir, f"{apk_name}_screenshots")

    if not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir)
        console.print(f"[green][+][/green] Created directory: {screenshot_dir}")

    # Search and modify secret words
    console.print("[magenta][*][/magenta][bold magenta] Searching for secret words...[/bold magenta]")
    found_any, found_words = searching_the_secret_word(root_directory, screenshot_dir, search_words_before_modification)
    console.print("\n" * 1)

    if found_any:
        console.print(f"[green][+][/green] Secret words found and screenshots taken.")
        console.print("[cyan]Found words:[/cyan]")
        for word, filepath, line_number in found_words:
            console.print(f"[white]\\_[/white][yellow]{word}[/yellow] found in [cyan]{filepath}[/cyan] at line [green]{line_number}[/green]")
    else:
        console.print("[yellow][!][/yellow] No secret words were found.")
    console.print("\n" * 2)

    console.print("[red][+][/red][bold red] Modifying secret words...[/bold red]")
    modify_secret_word(root_directory, search_words_before_modification)
    console.print("\n" * 1)

    # Check if the directory exists before recompiling
    if not os.path.exists(output_dir):
        console.print(f"[red][-][/red] [bold red]Error:[/bold red] APK decompilation directory not found: {output_dir}")
        sys.exit(1)

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

# Run the main function
if __name__ == "__main__":
    main()
