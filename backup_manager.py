#!/usr/bin/env python3

import sys
from utils.logger import log
from utils.aop import log_exceptions
# from utils.schedule import add_schedule, list_schedules, delete_schedule
# from utils.process import start_service, stop_service
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
        raise Exception("Simulated startup failure for testing purposes")
        # start_service()
        log("backup_service started")

   

    else:
        print(f"Unknown command: {command}")
        usage()


if __name__ == "__main__":
    main()
