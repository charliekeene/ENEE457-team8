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

# Object initialization
syn_flood_detect = syn_flood_detect.syn_flood_detect(ip_threshold=1000, total_threshold=5000, window_size=5)

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
print("Starting sniff")
sniff(iface=target_iface, prn=ids, count=0)