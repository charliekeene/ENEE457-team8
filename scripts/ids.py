from scapy.all import sniff

def packet_handler(packet):
    print(packet.summary())

print("Starting packet sniffer. Press Ctrl+C to stop.")

sniff(iface="eth0", prn=packet_handler, count=0)