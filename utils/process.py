import subprocess
import os
import signal
from typing import List
from utils.logger import log
from utils.aop import log_exceptions

PID_FILE = "backup_service.pid"

@log_exceptions(log, "start_service")
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


@log_exceptions(log, "stop_service")
def stop_service():
    if not os.path.exists(PID_FILE):
        msg = "Error: backup_service not running"
        print(msg)
        log(msg)
        return

    with open(PID_FILE, "r") as f:
        pid = int(f.read())

    log_path = os.path.join("logs", "backup_service", "latest.log")

    def _read_last_log_line(path: str):
        if not os.path.exists(path):
            return ""
        with open(path, "r") as lf:
            lines = [l.rstrip() for l in lf if l.strip()]
        return lines[-1] if lines else ""


    def _find_pids_by_name(name: str):

        out = subprocess.check_output(["ps", "aux"], text=True)
        pids = []
        for line in out.splitlines():
            if name in line:
                parts = line.split()
                if len(parts) >= 2:
                    p = int(parts[1])
                    pids.append(p)

        return pids

    last_line = _read_last_log_line(log_path).lower()
    is_exception = False
    if last_line:
        if "traceback" in last_line or "exception" in last_line:
            is_exception = True

    killed_any = False

    if is_exception:
        candidates = _find_pids_by_name("backup_service.py")
        for p in candidates:
            os.kill(p, signal.SIGTERM)
            killed_any = True
            log(f"Stopped backup_service (by name) PID={p}")

        if not killed_any:
            if pid:
                os.kill(pid, signal.SIGTERM)
                killed_any = True
                log(f"Stopped backup_service (by pid fallback) PID={pid}")

    else:
        if pid:
            proc_cmd = ""
            with open(f"/proc/{pid}/cmdline", "r") as pc:
                proc_cmd = pc.read()

            if "backup_service.py" in proc_cmd or "backup_service.py" in str(proc_cmd):
                os.kill(pid, signal.SIGTERM)
                killed_any = True
                log(f"Stopped backup_service (by pid) PID={pid}")
            else:
                # PID doesn't look like our process; try searching by name as safety
                candidates = _find_pids_by_name("backup_service.py")
                for p in candidates:
                    os.kill(p, signal.SIGTERM)
                    killed_any = True
                    log(f"Stopped backup_service (by name fallback) PID={p}")

    if not killed_any:
        msg = "Error: backup_service not running"
        print(msg)
        log(msg)
    else:
        if os.path.exists(PID_FILE):
            os.remove(PID_FILE)

        msg = "backup_service stopped"
        print(msg)
        log(msg)
