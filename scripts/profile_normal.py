import json
from packets_to_features import extract_features

# File path for baseline packet data (normal traffic only)
BASELINE_FILE = "data/features/packets_raw_baseline.csv"
# Output file to save the normal profile (thresholds, etc.)
PROFILE_OUTPUT_FILE = "data/features/normal_profile.json"

def build_profile(baseline_file=BASELINE_FILE):
    """
    Build a normal behavior profile from baseline packet data.
    Returns a dictionary containing baseline stats and recommended thresholds.
    """
    profile = {}
    # Extract SYN features from baseline data
    syn_counts = extract_features(baseline_file)
    if not syn_counts:
        print("Baseline data is empty or not found.")
        return None

    # Calculate the maximum SYN packets any source sent in a second during baseline
    max_syn_per_sec = 0
    total_syn = 0
    count_entries = 0
    # syn_counts keys are (src_ip, second), values are counts
    for (src, sec), count in syn_counts.items():
        total_syn += count
        count_entries += 1
        if count > max_syn_per_sec:
            max_syn_per_sec = count

    # Calculate average SYN per second per source (for info, not necessarily used for threshold)
    avg_syn_per_sec = (total_syn / count_entries) if count_entries > 0 else 0

    # Set threshold as, for example, 3 times the max normal SYN rate (you can adjust this as needed)
    threshold_syn_per_sec = 3 * max_syn_per_sec if max_syn_per_sec > 0 else 0

    # Prepare the profile dictionary
    profile['max_syn_per_sec'] = max_syn_per_sec
    profile['avg_syn_per_sec'] = avg_syn_per_sec
    profile['threshold_syn_per_sec'] = threshold_syn_per_sec

    # Save profile to a JSON file for later use
    try:
        with open(PROFILE_OUTPUT_FILE, 'w') as jf:
            json.dump(profile, jf, indent=4)
        print(f"Normal profile saved to {PROFILE_OUTPUT_FILE}")
    except Exception as e:
        print(f"Failed to save profile: {e}")
    return profile

# If run as a script, build the profile and print the results
if __name__ == "__main__":
    profile = build_profile()
    if profile:
        print("Normal Behavior Profile:")
        print(json.dumps(profile, indent=4))
