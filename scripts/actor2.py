# scripts/actor2.py

import time
import random

# File path to the shared raw packet log
LOG_FILE = "data/features/packets_raw.csv"

# Actor2 configuration (normal behavior)
SOURCE_IP = "10.0.0.2"        # IP address for actor2 (simulated)
DEST_IP = "10.0.0.100"        # Target server IP that actor2 is "accessing"
DEST_PORT = 80                # Target port (80 for HTTP for example)

def main():
    print("Actor2 (normal user) is starting.")
    # Normal user will send a request every few seconds
    interval = 5  # seconds between requests (can adjust as needed)
    # We will run for a certain duration then stop (so the container can exit)
    duration = 60  # seconds to run the simulation
    start_time = time.time()
    count = 0
    while True:
        current_time = time.time()
        elapsed = current_time - start_time
        if elapsed > duration:
            break  # Stop after the duration to end the simulation
        # Simulate sending a SYN packet to the server
        src_port = random.randint(1024, 65535)  # random source port
        timestamp = current_time
        log_line = f"{timestamp},{SOURCE_IP},{DEST_IP},{src_port},{DEST_PORT},SYN\n"
        try:
            # Open the log file in append mode and write the line
            with open(LOG_FILE, "a") as f:
                f.write(log_line)
        except Exception as e:
            # If file write fails, print error (in container logs)
            print(f"Actor2: Error writing to log file: {e}")
        print(f"Actor2: Sent SYN packet at time {timestamp}")  # console log for debug
        count += 1
        # Wait for the next interval
        time.sleep(interval)
    print(f"Actor2 finished sending {count} requests. Exiting.")

if __name__ == "__main__":
    main()
