import subprocess
import os
from rich.console import Console

# Initialize console for rich output
console = Console()

def sign_apk(apk_path, keystore_path, key_alias, keystore_password):
    """
    Function to sign an APK using jarsigner.
    
    :param apk_path: Path to the APK to be signed
    :param keystore_path: Path to the keystore file
    :param key_alias: Alias of the key in the keystore
    :param keystore_password: Password for the keystore
    """
    # Check if the APK file exists
    if not os.path.exists(apk_path):
        console.print(f"[red]APK file not found: {apk_path}[/red]")
        return
    
    # Check if the keystore file exists
    if not os.path.exists(keystore_path):
        console.print(f"[red]Keystore file not found: {keystore_path}[/red]")
        return

    try:
        # Command to sign the APK using jarsigner
        command = (
            f"jarsigner -verbose -keystore {keystore_path} "
            f"-storepass {keystore_password} "
            f"{apk_path} {key_alias}"
        )
        
        # Display processing message in green
        with console.status("[bold green]Signing APK, please wait...[/bold green]", spinner="dots"):
            # Execute the command using subprocess, but discard the output
            with open(os.devnull, 'w') as devnull:
                subprocess.check_call(command, shell=True, stdout=devnull, stderr=devnull)
        
        # Once done, print success message
        console.print("[green]APK signed successfully.[/green]")
        
    except subprocess.CalledProcessError as e:
        console.print(f"[red]Error signing APK: {e}[/red]")

