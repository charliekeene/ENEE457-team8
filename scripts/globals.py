# Utilities for time-stamped logging

import time
import os
from datetime import datetime

if "LOGFILE" not in globals():

    log_dir = "/app/logs"
    os.makedirs(log_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_filename = f"ids_{timestamp}.log"

    SIM_START_TIME = time.time()

    LOGFILE = open(os.path.join(log_dir, log_filename), "w")

# Write message to log with timestamp
def log(msg):
    uptime = time.time() - SIM_START_TIME
    LOGFILE.write(f"{uptime:.2f}, {msg}\n")
    LOGFILE.flush()