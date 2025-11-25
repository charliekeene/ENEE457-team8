# scripts/actor1.py

import time
import random

# File path to the shared raw packet log
LOG_FILE = "data/features/packets_raw.csv"

# Actor1 configuration (attack behavior)
SOURCE_IP = "10.0.0.1"        # IP address for actor1 (simulated attacker)
DEST_IP = "10.0.0.100"        # Target server IP that actor1 will attack (same as actor2's server)
DEST_PORT = 80                # Target port (attack the same service port)

def main():
    print("Actor1 (attacker) is starting.")
    # Wait for a short time before starting the attack.
    # This allows normal traffic to establish first.
    prep_time = 10  # seconds to wait before launching attack
    print(f"Actor1: Waiting for {prep_time} seconds before starting SYN flood...")
    time.sleep(prep_time)
    # Launch SYN flood attack
    flood_duration = 2      # attack duration in seconds (how long to send flood)
    send_rate = 100         # how many SYN packets to send per second during flood
    attack_start = time.time()
    packets_sent = 0
    while True:
        current_time = time.time()
        if current_time - attack_start > flood_duration:
            break  # end the attack after the duration has passed
        # Simulate sending a SYN packet (multiple per second)
        src_port = random.randint(1024, 65535)
        timestamp = current_time
        log_line = f"{timestamp},{SOURCE_IP},{DEST_IP},{src_port},{DEST_PORT},SYN\n"
        try:
            with open(LOG_FILE, "a") as f:
                f.write(log_line)
        except Exception as e:
            print(f"Actor1: Error writing to log file: {e}")
        packets_sent += 1
        # To achieve the desired send_rate, sleep accordingly.
        # send_rate = 100 per second means 0.01 sec between packets approximately.
        time.sleep(1.0 / send_rate)
    print(f"Actor1: SYN flood attack finished. Sent {packets_sent} SYN packets.")
    # Optionally, we could continue to run or send more bursts, but we'll stop after one attack.
    print("Actor1 is exiting now.")

if __name__ == "__main__":
    main()
