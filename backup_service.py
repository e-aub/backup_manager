import os
import tarfile
import time
from datetime import datetime
from utils.logger import RotatingLogger
from utils.aop import log_exceptions

SCHEDULES_FILE = "backup_schedules.txt"
BACKUPS_DIR = "./backups"
looger = RotatingLogger(log_dir="./logs/backup_service")

def ensure_backups_dir():
    if not os.path.exists(BACKUPS_DIR):
        os.makedirs(BACKUPS_DIR)
        looger.log(f"Created backups directory: {BACKUPS_DIR}")


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

@log_exceptions("create_backup")
def create_backup(path_to_save, backup_name):

    if not os.path.exists(path_to_save):
        looger.log(f"Error: Path does not exist: {path_to_save}")
        return False
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"{backup_name}.tar"
    backup_path = os.path.join(BACKUPS_DIR, backup_filename)
    

    with tarfile.open(backup_path, "w:gz") as tar:
        tar.add(path_to_save, arcname=os.path.basename(path_to_save))
    looger.log(f"Backup created successfully: {backup_path}")
    return True

def check_and_run_backups():
    current_time = datetime.now().strftime("%H:%M")
    schedules = read_schedules()
    
    for schedule in schedules:
        if schedule["time"] == current_time:
            looger.log(f"Running scheduled backup: {schedule['name']}")
            create_backup(schedule["path"], schedule["name"])


def main():
    looger.log("Backup Service started.")
    looger.log(f"Reading schedules from: {SCHEDULES_FILE}")
    looger.log(f"Saving backups to: {BACKUPS_DIR}")
    looger.log("-" * 40)
    
    ensure_backups_dir()
    
    while True:
        check_and_run_backups()
        time.sleep(45)


if __name__ == "__main__":
    main()
