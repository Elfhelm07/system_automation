import subprocess
import time
from datetime import datetime, timedelta

def create_restore_point():
    try:
        subprocess.run(["powershell", "Checkpoint-Computer", "-Description", "Automatic Restore Point", "-RestorePointType", "MODIFY_SETTINGS"], check=True)
        print(f"Restore point created at {datetime.now()}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to create restore point: {e}")

def schedule_restore_points(x_days):
    interval = timedelta(days=x_days)
    while True:
        create_restore_point()
        print(f"Next restore point will be created in {x_days} days.")
        time.sleep(interval.total_seconds())
