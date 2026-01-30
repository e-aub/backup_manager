import subprocess
import os
import signal
from utils.logger import log
from utils.aop import log_exceptions

PID_FILE = "backup_service.pid"

@log_exceptions("start_service")
def start_service():
    if os.path.exists(PID_FILE):
        msg = "Error: backup_service already running"
        print(msg)
        log(msg)
        return

    proc = subprocess.Popen(
        ["python3", "backup_service.py"],
        start_new_session=True
    )
    with open(PID_FILE, "w") as f:
        f.write(str(proc.pid))

    msg = f"backup_service started with PID {proc.pid}"
    print(msg)
    log(msg)


@log_exceptions("stop_service")
def stop_service():
    if not os.path.exists(PID_FILE):
        msg = "Error: backup_service not running"
        print(msg)
        log(msg)
        return

    with open(PID_FILE, "r") as f:
        pid = int(f.read())

    try:
        os.kill(pid, signal.SIGTERM)
    except ProcessLookupError:
        msg = "Error: backup_service not running"
        print(msg)
        log(msg)

    if os.path.exists(PID_FILE):
        os.remove(PID_FILE)

    msg = "backup_service stopped"
    print(msg)
    log(msg)
