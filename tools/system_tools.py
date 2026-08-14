import subprocess
import json

def open_windows_app(app_name: str) -> str:
    """
    Launches an application on the Windows host machine from WSL.
    
    Args:
        app_name (str): The executable name or common name of the app (e.g., 'notepad', 'calc', 'spotify').
    """
    try:
        print(f"[DEMON Cell Tool]: Attempting to open {app_name}...")
        subprocess.run(
            ["powershell.exe", "-Command", f"Start-Process {app_name}"], 
            check=True, 
            capture_output=True
        )
        return f"Successfully opened {app_name} on the host machine."
    except subprocess.CalledProcessError as e:
        return f"Failed to open {app_name}. Make sure the application name is correct. Error: {e.stderr.decode().strip()}"

def adjust_volume(action: str) -> str:
    """
    Adjusts the Windows system volume.
    
    Args:
        action (str): Must be 'up', 'down', or 'mute'.
    """
    # Using Windows Script Host Shell to send virtual keypresses for media controls
    key_codes = {
        "mute": "173",
        "down": "174",
        "up": "175"
    }
    
    if action not in key_codes:
        return "Invalid volume action. Use 'up', 'down', or 'mute'."
        
    try:
        print(f"[DEMON Cell Tool]: Adjusting volume ({action})...")
        ps_command = f"$obj = new-object -com wscript.shell; $obj.SendKeys([char]{key_codes[action]})"
        subprocess.run(["powershell.exe", "-Command", ps_command], check=True)
        return f"System volume successfully turned {action}."
    except Exception as e:
        return f"Failed to adjust volume: {str(e)}"

def check_system_status() -> str:
    """
    Retrieves the current CPU and RAM usage of the Windows host machine.
    """
    try:
        print("[DEMON Cell Tool]: Polling system status...")
        # Get CPU Load
        cpu_cmd = "(Get-CimInstance Win32_Processor | Measure-Object -Property LoadPercentage -Average).Average"
        cpu_result = subprocess.run(["powershell.exe", "-Command", cpu_cmd], capture_output=True, text=True)
        cpu_usage = cpu_result.stdout.strip()

        # Get Free RAM (in GB)
        ram_cmd = "[math]::Round((Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory / 1MB, 2)"
        ram_result = subprocess.run(["powershell.exe", "-Command", ram_cmd], capture_output=True, text=True)
        free_ram = ram_result.stdout.strip()

        return f"Host System Status: CPU is currently at {cpu_usage}% load. There is {free_ram} GB of available RAM."
    except Exception as e:
        return f"Failed to retrieve system status: {str(e)}"