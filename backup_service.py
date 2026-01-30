import os
import tarfile
import time
from datetime import datetime

SCHEDULES_FILE = "backup_schedules.txt"
BACKUPS_DIR = "./backups"


def ensure_backups_dir():
    if not os.path.exists(BACKUPS_DIR):
        os.makedirs(BACKUPS_DIR)
        print(f"Created backups directory: {BACKUPS_DIR}")


def read_schedules():
    schedules = []
    if not os.path.exists(SCHEDULES_FILE):
        return schedules
    
    with open(SCHEDULES_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(";")
            if len(parts) == 3:
                path_to_save, schedule_time, backup_name = parts
                schedules.append({
                    "path": path_to_save,
                    "time": schedule_time,
                    "name": backup_name
                })
    return schedules


def create_backup(path_to_save, backup_name):

    if not os.path.exists(path_to_save):
        print(f"Error: Path does not exist: {path_to_save}")
        return False
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"{backup_name}_{timestamp}.tar.gz"
    backup_path = os.path.join(BACKUPS_DIR, backup_filename)
    
    try:
        with tarfile.open(backup_path, "w:gz") as tar:
            tar.add(path_to_save, arcname=os.path.basename(path_to_save))
        print(f"Backup created successfully: {backup_path}")
        return True
    except Exception as e:
        print(f"Error creating backup: {e}")
        return False


def check_and_run_backups():
    current_time = datetime.now().strftime("%H:%M")
    schedules = read_schedules()
    
    for schedule in schedules:
        if schedule["time"] == current_time:
            print(f"Running scheduled backup: {schedule['name']}")
            create_backup(schedule["path"], schedule["name"])


def main():
    print("Backup Service started.")
    print(f"Reading schedules from: {SCHEDULES_FILE}")
    print(f"Saving backups to: {BACKUPS_DIR}")
    print("-" * 40)
    
    ensure_backups_dir()
    
    while True:
        check_and_run_backups()
        time.sleep(45)


if __name__ == "__main__":
    main()
