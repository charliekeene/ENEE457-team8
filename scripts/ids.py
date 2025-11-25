from scapy.all import sniff, TCP, IP
import time
import syn_flood_detect
from globals import log

# Main IDS function
# Put any packet detection methods in here
def ids(packet):
    # print(packet.summary()) # <- used to test, but this will spam the console so double Ctrl-C to stop
    syn_flood_detect.process_packet(packet)

# Object initialization
syn_flood_detect = syn_flood_detect.syn_flood_detect(ip_threshold=1000, total_threshold=5000, window_size=5)

print("Starting sniff")
sniff(iface="eth1", prn=ids, count=0)