#start the following apps on startup or on demand
import os
import json
import subprocess
import keyboard
from pathlib import Path
from win32com.client import Dispatch

STARTUP_FOLDER = r"C:\Users\Lenovo\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup"

def load_app_config():
    config_path = Path(os.path.expanduser("~")) / ".app_launcher_config.json"
    if config_path.exists():
        with open(config_path, "r") as f:
            return json.load(f)
    return {"keybind_apps": []}

def save_app_config(config):
    config_path = Path(os.path.expanduser("~")) / ".app_launcher_config.json"
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)

def create_shortcut(target_path, shortcut_name):
    shortcut_path = os.path.join(STARTUP_FOLDER, f"{shortcut_name}.lnk")
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(shortcut_path)
    shortcut.Targetpath = target_path
    shortcut.WorkingDirectory = os.path.dirname(target_path)
    shortcut.save()
    print(f"Created startup shortcut for {shortcut_name} at {shortcut_path}")

def launch_app(app_path):
    try:
        subprocess.Popen(app_path)
        print(f"Launched: {app_path}")
    except Exception as e:
        print(f"Error launching {app_path}: {e}")

def setup_keybindings():
    config = load_app_config()
    for app in config["keybind_apps"]:
        print(f"Setting up keybind: {app['keybind']} for {app['path']}")
        keyboard.add_hotkey(app["keybind"], lambda path=app["path"]: launch_app(path))
    print("Keybindings setup complete.")

def add_app_to_config():
    config = load_app_config()
    name = input("Enter the application name: ")
    path = input("Enter the full path to the application: ")
    launch_type = input("Add to (1) startup or (2) keybind? Enter 1 or 2: ")
    if launch_type == "1":
        create_shortcut(path, name)
    elif launch_type == "2":
        keybind = input("Enter the keybind (e.g., 'ctrl+shift+k'): ")
        config["keybind_apps"].append({"name": name, "path": path, "keybind": keybind})
        save_app_config(config)
        print(f"Added {name} to keybind configuration")
    else:
        print("Invalid choice. App not added.")

def launch_startup_apps():
    for item in os.listdir(STARTUP_FOLDER):
        if item.endswith('.lnk'):
            shortcut_path = os.path.join(STARTUP_FOLDER, item)
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(shortcut_path)
            target_path = shortcut.Targetpath
            launch_app(target_path)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--add-app":
        add_app_to_config()
    elif len(sys.argv) > 1 and sys.argv[1] == "--launch-startup":
        launch_startup_apps()
    else:
        setup_keybindings()
        print("Keybinding setup complete. Press Ctrl+C to exit.")
        keyboard.wait()