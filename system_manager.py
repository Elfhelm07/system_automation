import sys
from databackup import schedule_restore_points
from app_launcher import add_app_to_config, launch_startup_apps, setup_keybindings
from autoupdate import get_winget_upgrades
import keyboard

def print_instructions():
    print("Usage: python system_manager.py <command> [options]")
    print("Commands:")
    print("  --create-restore-point <days>  Create a system restore point every <days> days")
    print("  --add-app                      Add an application to startup or keybind")
    print("  --launch-startup               Launch all startup applications")
    print("  --setup-keybindings            Setup keybindings for applications")
    print("  --update-apps                  Update applications using winget")
    print("  --help                         Show this help message")

def main():
    if len(sys.argv) < 2:
        print_instructions()
        return

    command = sys.argv[1]
    if command == "--help":
        print_instructions()
        return
    elif command == "--create-restore-point":
        if len(sys.argv) < 3:
            print("Please specify the number of days between restore points.")
            return
        x_days = int(sys.argv[2])
        schedule_restore_points(x_days)
    elif command == "--add-app":
        add_app_to_config()
    elif command == "--launch-startup":
        launch_startup_apps()
    elif command == "--setup-keybindings":
        setup_keybindings()
        print("Keybinding setup complete. Press Ctrl+C to exit.")
        keyboard.wait()
    elif command == "--update-apps":
        get_winget_upgrades()
    else:
        print("Unknown command.")
        print_instructions()

if __name__ == "__main__":
    print_instructions()  # Print instructions when the script is run
    main()
