# Overview: This file contains code to detect a SYN-ACK Denial of Service Attack
# Primary Author: Graham Rogers
# Description: A SYN-ACK is a Denial of Service attack in which a large number of handshakes are initiated with a server
# without completion. The result is that the server must manage a large amount of these unfinished handshakes resulting in a
# large consumption of resources and therefore a denial of resources towards normal usage.

from scapy.all import sniff, TCP, IP
import time

# --- Parameters ---
TARGET_PORTS = [80, 443] # List of important ports to monitor
IP_THRESHOLD = 50   # Number of acceptable SYN packets from a given IP (DoS)
TOTAL_THRESHOLD = 500   # Number of acceptable SYN packets on a total port (DDoS)
WINDOW_SIZE = 5 # Size in seconds of a given measuring window

# --- State Variables ---
syn_counts = {}
last_check_time = time.time() # Initialize to current time
total_syn_count = 0

# Create the Scapy filter string from the TARGET_PORTS list
port_filter = " or ".join([f"port {p}" for p in TARGET_PORTS])
SCAPY_FILTER = f"tcp and ({port_filter})"

def check_for_reset():
    global last_check_time
    global syn_counts
    global total_syn_count

    current_time = time.time()
    # Check is window is finished and if so, reset system
    if (current_time - last_check_time) >= WINDOW_SIZE:
        syn_counts = {}
        last_check_time = current_time
        total_syn_count = 0

def detect_syn_attack(packet):
    global syn_counts
    global total_syn_count
    
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
            
            print(f"[*] SYN from {src_ip} to port {dport}. Count: {syn_counts[key]}")
            
            # DoS Check
            if syn_counts[key] > IP_THRESHOLD:
                print(f"*** ALERT: IP {src_ip} hitting Port {dport} ***")
                print(f"    SYN Count {syn_counts[key]} > Threshold {IP_THRESHOLD}")

            # DDoS Check
            if total_syn_count > TOTAL_THRESHOLD:
                print(f"*** ALERT: Port {dport} is flooded from multiple IP addresses ***")
                print(f"    SYN Count {syn_counts[key]} > Threshold {TOTAL_THRESHOLD}")

    # Run the reset check
    check_for_reset()

print(f"Monitoring ports {TARGET_PORTS} for SYN Floods...")
print(f"Scapy Filter: {SCAPY_FILTER}")

# Sniff packets based on port/protoccol
sniff(prn=detect_syn_attack, filter=SCAPY_FILTER, store=0)