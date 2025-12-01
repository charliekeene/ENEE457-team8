import csv, json

syn_counts = {}  # nested dict: syn_counts[ip][second] = count
# Read the baseline CSV
with open('data/packets_raw_baseline.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        src_ip = row['SourceIP']
        flags = row['Flags']  # assuming there's a Flags column
        timestamp = float(row['Timestamp'])  # epoch time or similar
        if 'S' in flags:  # or flags == 'SYN', depending on format
            sec = int(timestamp)  # second-granularity
            # Initialize nested dict if not present
            if src_ip not in syn_counts:
                syn_counts[src_ip] = {}
            # Increment count for that second
            syn_counts[src_ip][sec] = syn_counts[src_ip].get(sec, 0) + 1

# Compute max SYN rate per IP
thresholds = {}
for ip, counts in syn_counts.items():
    max_rate = max(counts.values())
    thresholds[ip] = max_rate * 3  # 3x rule

# Save to JSON
with open('data/normal_profile.json', 'w') as f:
    json.dump(thresholds, f, indent=4)
