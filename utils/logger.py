import os
import datetime
import time

LOG_DIR = "../logs"
MAX_LOG_SIZE = 1024 

class RotatingLogger:
    def __init__(self, log_dir=LOG_DIR, max_size=MAX_LOG_SIZE):
        self.log_dir = log_dir
        self.max_size = max_size
        os.makedirs(log_dir, exist_ok=True)

        self.start_time = datetime.datetime.now()
        self.current_file = os.path.join(self.log_dir, "latest.log")

        self.rotation_index = 0

    def _timestamp(self):
        return datetime.datetime.now().strftime("%d/%m/%Y %H:%M")

    def _rotate(self):
        end_time = datetime.datetime.now()

        start_str = self.start_time.strftime("%Y-%m-%d_%H:%M:%S")
        end_str = end_time.strftime("%Y-%m-%d_%H:%M:%S")

        while True:
            suffix = f"_{self.rotation_index}" if self.rotation_index else ""
            new_name = os.path.join(
                self.log_dir,
                f"from_{start_str}_to_{end_str}{suffix}.log"
            )
            if not os.path.exists(new_name):
                break
            self.rotation_index += 1

        os.rename(self.current_file, new_name)

        self.start_time = datetime.datetime.now()
        self.rotation_index = 0

    def log(self, message: str):
        with open(self.current_file, "a") as f:
            f.write(f"[{self._timestamp()}] {message}\n")

        if os.path.getsize(self.current_file) >= self.max_size:
            self._rotate()


logger = RotatingLogger()
log = logger.log
while True:
    log("This is a test log message.")
    time.sleep(1)