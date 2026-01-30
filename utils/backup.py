import os
from utils.logger import log
from utils.aop import log_exceptions

BACKUP_DIR = "backups"

@log_exceptions(log, "list_backups")
def list_backups():
    if not os.path.exists(BACKUP_DIR):
        msg = "Error: can't find backups directory"
        print(msg)
        log(msg)
        return []

    files = [f for f in os.listdir(BACKUP_DIR) if f.endswith(".tar")]
    log("Show backups list")
    return files
