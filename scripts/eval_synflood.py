import sys
from profile_normal import build_profile
from detect_synflood_rules import detect_syn_flood

if __name__ == "__main__":
    # Optionally accept command-line arguments for file paths
    baseline_file = "data/features/packets_raw_baseline.csv"
    current_file = "data/features/packets_raw.csv"
    if len(sys.argv) >= 3:
        baseline_file = sys.argv[1]
        current_file = sys.argv[2]
    print(f"Using baseline file: {baseline_file}")
    print(f"Using current data file: {current_file}")
    # Build profile from baseline
    profile = build_profile(baseline_file=baseline_file)
    if profile is None:
        sys.exit("Baseline profile could not be created. Exiting.")
    # Run detection on current data
    anomalies = detect_syn_flood(data_file=current_file, profile_file="data/features/normal_profile.json")
    print(f"Anomaly detection done. Found {len(anomalies)} anomaly events.")
    if anomalies:
        print("Anomalies:")
        for a in anomalies:
            print(a)
