# scripts/packets_to_features.py
import csv
from collections import defaultdict
from datetime import datetime

# File path for raw packet data (adjust if needed based on actual volume mount)
RAW_PACKET_FILE = "data/features/packets_raw.csv"

def extract_features(raw_file=RAW_PACKET_FILE, flag_filter="SYN"):
    """
    Read raw packet data from CSV and extract features.
    Returns a dictionary: { (source_ip, second) : count }
    where 'second' is a timestamp (rounded to integer seconds) and count is
    the number of packets matching `flag_filter` from source_ip in that second.

    `flag_filter` is a string like 'SYN' or 'ICMP'. Default is 'SYN' for backwards
    compatibility with existing code.
    """
    counts = defaultdict(int)
    try:
        with open(raw_file, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                # Each row expected format: time, src_ip, dst_ip, src_port, dst_port, flag
                # Example: 1637768400.1234,10.0.0.2,10.0.0.100,12345,80,SYN
                if not row or row[0].startswith("#"):
                    # Skip empty lines or comments
                    continue
                # guard against rows that don't have expected columns
                if len(row) < 6:
                    continue
                timestamp_str, src_ip, dst_ip, src_port, dst_port, flag = row[:6]
                # Match the requested flag (case-insensitive)
                if flag.strip().upper() == flag_filter.strip().upper():
                    try:
                        ts = float(timestamp_str)
                    except ValueError:
                        # If timestamp is not a float (unexpected format), skip this row
                        continue
                    second = int(ts)
                    # Use (source_ip, second) as key
                    key = (src_ip, second)
                    counts[key] += 1
    except FileNotFoundError:
        print(f"Raw packet file not found: {raw_file}")
    return counts

# If run as a script, extract features and print a summary
if __name__ == "__main__":
    features = extract_features()
    # Print out the feature counts for verification
    # (We will typically use these counts in detection rather than just printing)
    for key, count in features.items():
        src_ip, second = key
        if count > 0:
            # Format the second as a human-readable time for display
            time_str = datetime.fromtimestamp(second).strftime("%Y-%m-%d %H:%M:%S")
            print(f"{time_str} - {src_ip} sent {count} SYN packets")
