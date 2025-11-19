from scapy.all import sniff, TCP, IP
import syn_flood_detect as syn_flood_detect

# Main IDS function
# Put any packet detection methods in here
def ids(packet):
    syn_flood_detect.detect_syn_attack(packet)

# Sniff all packets on eth0
# Filters can be added as desired (e.g. TCP only, certain ports, etc.)
sniff(iface="eth0", prn=ids, count=0, store=0)