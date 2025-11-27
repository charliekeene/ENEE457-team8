import json
from datetime import datetime
from packets_to_features import extract_features

# File paths for current run data and profile
CURRENT_DATA_FILE = "data/features/packets_raw.csv"
PROFILE_FILE = "data/features/normal_profile.json"
ANOMALY_LOG_FILE = "data/features/anomalies.log" 

def detect_icmp_flood(data_file=CURRENT_DATA_FILE, profile_file=PROFILE_FILE):
    """
    Detect ICMP flood attacks by comparing current data to normal profile thresholds.
    Writes any detected anomalies to a log file and returns a list of detected events.
    """
    # Load normal profile (thresholds) from JSON
    try:
        with open(profile_file, 'r') as pf:
            profile = json.load(pf)
    except FileNotFoundError:
        print("Normal profile file not found. Please run profile_normal.py first.")
        return []
    except json.JSONDecodeError:
        print("Error reading the profile file (invalid JSON).")
        return []

    # Get the threshold for ICMP packets per second from profile
    # We expect the profile to include a key like "threshold_icmp_per_sec"
    threshold = profile.get("threshold_icmp_per_sec", None)
    if threshold is None:
        print("ICMP threshold value not found in profile.")
        return []

    # Extract ICMP counts from current data (packets_to_features should provide per-(src,second) counts)
    icmp_counts = extract_features(data_file)
    anomalies = []  # to store detected anomaly events

    # Check each source-second pair in current data for threshold breach
    for (src_ip, second), count in icmp_counts.items():
        if count > threshold:
            # We found an anomaly: this src_ip sent more ICMPs in one second than the threshold.
            event_time = datetime.fromtimestamp(second).strftime("%Y-%m-%d %H:%M:%S")
            anomaly = {
                "time": event_time,
                "source_ip": src_ip,
                "icmp_count": count,
                "threshold": threshold,
                "description": "ICMP flood suspected: too many ICMP Echo Requests"
            }
            anomalies.append(anomaly)
            # Log the anomaly event to the console for immediate feedback
            print(f"[ALERT] {src_ip} sent {count} ICMP packets at {event_time} (threshold {threshold})")

    # Write anomalies to log file in JSON lines format
    if anomalies:
        try:
            with open(ANOMALY_LOG_FILE, 'a') as logf:
                for anomaly in anomalies:
                    logf.write(json.dumps(anomaly) + "\n")
        except Exception as e:
            print(f"Error writing to ICMP anomaly log file: {e}")
    else:
        print("No ICMP flood detected in current data.")
    return anomalies


if __name__ == "__main__":
    detected = detect_icmp_flood()
    print(f"Detection complete. Total ICMP anomalies found: {len(detected)}")
    if detected:
        print(f"Details are logged in {ANOMALY_LOG_FILE}")
