#!/usr/bin/env python3

import sys
from utils.logger import log
from utils.aop import log_exceptions
# from utils.schedule import add_schedule, list_schedules, delete_schedule
from utils.process import start_service, stop_service
# from utils.backup import list_backups


def usage():
    print(
        "Usage:\n"
        "  backup_manager.py start\n"
        "  backup_manager.py stop\n"
        "  backup_manager.py create \"path;hh:mm;backup_name\"\n"
        "  backup_manager.py list\n"
        "  backup_manager.py delete INDEX\n"
        "  backup_manager.py backups\n"
        "  backup_manager.py --help\n"
    )


@log_exceptions("backup_manager entry point")
def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("--help", "-h"):
        usage()
        return

    command = sys.argv[1]

    if command == "start":
        start_service()

    elif command == "stop":
        stop_service()

    elif command == "create":
        if len(sys.argv) != 3:
            print("Error: missing schedule")
            usage()
            return
        schedule = sys.argv[2]
        add_schedule(schedule)
        log(f"New schedule added: {schedule}")

    elif command == "list":
        schedules = list_schedules()
        for i, s in enumerate(schedules):
            print(f"{i}: {s}")
        log("Show schedules list")

    elif command == "delete":
        if len(sys.argv) != 3 or not sys.argv[2].isdigit():
            print("Error: invalid index")
            usage()
            return
        index = int(sys.argv[2])
        delete_schedule(index)
        log(f"Schedule at index {index} deleted")

    elif command == "backups":
        backups = list_backups()
        for b in backups:
            print(b)
        log("Show backups list")

    else:
        print(f"Unknown command: {command}")
        usage()


if __name__ == "__main__":
    main()
