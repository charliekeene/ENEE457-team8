from scapy.all import sniff, TCP, IP
import time
import syn_flood_detect
from globals import log
import subprocess
import re
import fingerprint

# Main IDS function
# Put any packet detection methods in here
def ids(packet):
    # print(packet.summary()) # <- used to test, but this will spam the console so double Ctrl-C to stop
    fingerprint.process_packet(packet)
    syn_flood_detect.process_packet(packet)
    fingerprint_detector.process_packet(packet)

# Object initialization
fingerprint = fingerprint.Fingerprint("scripts/fingerprint_rules.json")
syn_flood_detect = syn_flood_detect.syn_flood_detect(ip_threshold=1000, total_threshold=5000, window_size=5)
fingerprint_detector = fingerprint.Fingerprint("scripts/fingerprint_rules.json")

result = subprocess.run(
        ["ip", "-o", "addr", "show"],
        capture_output=True,
        text=True
    )

target_iface=""

for line in result.stdout.splitlines():
    # Example line: "3: eth0    inet 172.17.0.2/16 ..."
    match = re.search(r'\d+:\s+(\S+)\s+.*inet\s+(\d+\.29\.\d+\.\d+)/', line)
    if match:
        iface, ip = match.groups()
        target_iface = iface 

subprocess.run(["ip", "link", "set", target_iface, "promisc", "on"])

# Sniff all packets on eth0
# Filters can be added as desired (e.g. TCP only, certain ports, etc.)
print(f"Using interface: {target_iface}")
print("Starting sniff")
sniff(iface=target_iface, prn=ids, store=False, count=0)
