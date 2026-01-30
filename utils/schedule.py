import os
from utils.logger import log
from utils.aop import log_exceptions

SCHEDULE_FILE = "backup_schedules.txt"

@log_exceptions(log, "add_schedule")
def add_schedule(schedule: str):
    parts = schedule.strip().split(";")
    if len(parts) != 3:
        msg = f"Error: malformed schedule: {schedule}"
        print(msg)
        log(msg)
        return

    with open(SCHEDULE_FILE, "a") as f:
        f.write(schedule + "\n")

    msg = f"New schedule added: {schedule}"
    print(msg)
    log(msg)


@log_exceptions(log, "list_schedules")
def list_schedules():
    if not os.path.exists(SCHEDULE_FILE):
        msg = "Error: can't find backup_schedules.txt"
        print(msg)
        log(msg)
        return []

    with open(SCHEDULE_FILE, "r") as f:
        schedules = [line.strip() for line in f.readlines() if line.strip()]

    log("Show schedules list")
    return schedules


@log_exceptions(log, "delete_schedule")
def delete_schedule(index: int):
    if not os.path.exists(SCHEDULE_FILE):
        msg = "Error: can't find backup_schedules.txt"
        print(msg)
        log(msg)
        return

    with open(SCHEDULE_FILE, "r") as f:
        lines = [line for line in f.readlines() if line.strip()]

    if index < 0 or index >= len(lines):
        msg = f"Error: can't find schedule at index {index}"
        print(msg)
        log(msg)
        return

    lines.pop(index)
    with open(SCHEDULE_FILE, "w") as f:
        f.writelines(lines)

    msg = f"Schedule at index {index} deleted"
    print(msg)
    log(msg)
