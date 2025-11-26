from scapy.all import sniff, TCP, IP
import time
import syn_flood_detect
from globals import log
import subprocess
import re

# Main IDS function
# Put any packet detection methods in here
def ids(packet):
    # print(packet.summary()) # <- used to test, but this will spam the console so double Ctrl-C to stop
    syn_flood_detect.process_packet(packet)
    print(packet.summary())

# Object initialization
syn_flood_detect = syn_flood_detect.syn_flood_detect(ip_threshold=1000, total_threshold=5000, window_size=5)

    # State Variables
    syn_counts = {}
    last_check_time = time.time() # Initialize to current time
    total_syn_count = 0
    detected = 0
    
    # Check if the packet has TCP and IP layers
    if packet.haslayer(TCP) and packet.haslayer(IP):
        
        # Check if the packet has only the SYN flag set (no ACK)
        # 0x02 is the numeric value for the SYN flag
        if packet[TCP].flags == 0x02:

            total_syn_count += 1
            
            src_ip = packet[IP].src
            dport = packet[TCP].dport
            key = (src_ip, dport)
            
            # Increment the counter for the unique key (source IP, dest port)
            syn_counts[key] = syn_counts.get(key, 0) + 1
            
            # Detect SYN Flood (only one detection/report per window)

            # DoS Check
            if (syn_counts[key] > IP_THRESHOLD) and (detected == 0):
                print(f"ANOMALY: SYN Flood (DoS), {src_ip}, {dport}")
                detected = 1

            # DDoS Check
            if (total_syn_count > TOTAL_THRESHOLD) and (detected == 0):
                print(f"ANOMALY: SYN Flood (DDoS), n/a, {dport}")
                detected = 1

    current_time = time.time()
    # Check is window is finished and if so, reset system
    if (current_time - last_check_time) >= WINDOW_SIZE:
        syn_counts = {}
        last_check_time = current_time
        total_syn_count = 0
        detected = 0

result = subprocess.run(
        ["ip", "-o", "addr", "show"],
        capture_output=True,
        text=True
    )

target_iface=""

for line in result.stdout.splitlines():
    # Example line: "3: eth0    inet 172.17.0.2/16 ..."
    match = re.search(r'\d+:\s+(\S+)\s+.*inet\s+(\d+\.\d+\.\d+\.\d+)/', line)
    if match:
        iface, ip = match.groups()
        if ip == "172.29.0.1":
            target_iface = iface 

# Sniff all packets on eth0
# Filters can be added as desired (e.g. TCP only, certain ports, etc.)
print("Starting sniff")
sniff(iface=target_iface, prn=ids, count=0)