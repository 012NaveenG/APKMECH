import subprocess
import os
from rich.console import Console

# Initialize console for rich output
console = Console()

def run_command(command):
    try:
        with open(os.devnull, 'w') as devnull:
            subprocess.check_call(command, shell=True, stdout=devnull, stderr=devnull)
    except subprocess.CalledProcessError as e:
        console.print(f"[red]Error executing command: {e}[/red]")

def recompile_apk(decompiled_apk_dir, recompile_apk_path):
    """
    Function to recompile APK using apktool.
    
    :param decompiled_apk_dir: Directory where APK has been decompiled
    :param recompile_apk_path: Output path where the recompiled APK will be saved
    """
    apktool_bat_path = os.path.join(os.getcwd(), "tools", "apktool", "apktool.bat")
    
    if os.name == 'nt':
        if os.path.exists(apktool_bat_path):
            command = f"java -jar {apktool_bat_path} b {decompiled_apk_dir} -o {recompile_apk_path}"
        else:
            console.print("[red]apktool.bat not found[/red]")
            return
    else:
        apk_tool_for_linux = os.path.join(os.getcwd(), "tools", "apktool", "apktool.jar")
        command = f"java -jar {apk_tool_for_linux} b {decompiled_apk_dir} -o {recompile_apk_path}"
    
    # Display progress message while recompiling the APK
    with console.status("[bold green]Recompiling APK, please wait...[/bold green]", spinner="dots"):
        run_command(command)
    
    console.print(f"[green]APK recompiled successfully: {recompile_apk_path}[/green]")

