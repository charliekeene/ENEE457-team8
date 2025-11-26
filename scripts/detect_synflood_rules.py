import json
from datetime import datetime
from packets_to_features import extract_features

# File paths for current run data and profile
CURRENT_DATA_FILE = "data/features/packets_raw.csv"
PROFILE_FILE = "data/features/normal_profile.json"
ANOMALY_LOG_FILE = "data/features/anomalies.log"  # where we record detection results

def detect_syn_flood(data_file=CURRENT_DATA_FILE, profile_file=PROFILE_FILE):
    """
    Detect SYN flood attacks by comparing current data to normal profile thresholds.
    Writes any detected anomalies to a log file.
    Returns a list of detected anomaly events.
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

    # Get the threshold for SYN packets per second from profile
    threshold = profile.get("threshold_syn_per_sec", None)
    if threshold is None:
        print("Threshold value not found in profile.")
        return []

    # Extract SYN counts from current data
    syn_counts = extract_features(data_file)
    anomalies = []  # to store detected anomaly events

    # Check each source-second pair in current data for threshold breach
    for (src_ip, second), count in syn_counts.items():
        if count > threshold:
            # We found an anomaly: this src_ip sent more SYNs in one second than the threshold.
            event_time = datetime.fromtimestamp(second).strftime("%Y-%m-%d %H:%M:%S")
            anomaly = {
                "time": event_time,
                "source_ip": src_ip,
                "syn_count": count,
                "threshold": threshold,
                "description": "SYN flood suspected: too many SYN packets"
            }
            anomalies.append(anomaly)
            # Log the anomaly event to the console for immediate feedback
            print(f"[ALERT] {src_ip} sent {count} SYN packets at {event_time} (threshold {threshold})")

    # Write anomalies to log file in JSON lines format
    if anomalies:
        try:
            with open(ANOMALY_LOG_FILE, 'a') as logf:
                for anomaly in anomalies:
                    # Write each anomaly as a JSON object on a new line
                    logf.write(json.dumps(anomaly) + "\n")
        except Exception as e:
            print(f"Error writing to anomaly log file: {e}")
    else:
        print("No SYN flood detected in current data.")
    return anomalies

# If run as a script, perform detection and notify the user
if __name__ == "__main__":
    detected = detect_syn_flood()
    print(f"Detection complete. Total anomalies found: {len(detected)}")
    if detected:
        print(f"Details are logged in {ANOMALY_LOG_FILE}")
