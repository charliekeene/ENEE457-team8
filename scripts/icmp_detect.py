# ICMP attack detector, modeled after syn_flood_detect.py
# Provides a class called icmp_flood_detect and calls process_packet(packet) for each captured packet.
# Uses log() to match existing logging technique.
# Only detects ICMP Echo Request floods (which are type 8).

from scapy.all import ICMP, IP
from globals import log
import time

class icmp_flood_detect:
    def __init__(self, ip_threshold=1000, total_threshold=5000, window_size=5):
        # Thresholds set
        self.IP_THRESHOLD = ip_threshold    # Echo Requests per source IP
        self.TOTAL_THRESHOLD = total_threshold  # Total ICMP Echo Requests
        self.WINDOW_SIZE = window_size  # Time window in seconds

        # State
        self.icmp_counts = {}
        self.total_icmp_count = 0
        self.last_check_time = time.time()
        self.detected = False

    def process_packet(self, packet):
        # Again, only considering type 8 packets (this is basically a ping request)
        if packet.haslayer(ICMP) and packet.haslayer(IP):
            icmp_layer = packet[ICMP]
            if getattr(icmp_layer, 'type', None) == 8:
                self.total_icmp_count += 1

                src_ip = packet[IP].src
                self.icmp_counts[src_ip] = self.icmp_counts.get(src_ip, 0) + 1

                # DoS Check (per-source)
                if (self.icmp_counts[src_ip] > self.IP_THRESHOLD) and (self.detected == False):
                    log(f"ICMP Flood (DoS), {src_ip}")
                    self.detected = True

                # DDoS Check (aggregate)
                if (self.total_icmp_count > self.TOTAL_THRESHOLD) and (self.detected == False):
                    log(f"ICMP Flood (DDoS), n/a")
                    self.detected = True

        current_time = time.time()
        # Check if the window is finished and if so, reset system
        if (current_time - self.last_check_time) >= self.WINDOW_SIZE:
            self.icmp_counts = {}
            self.last_check_time = current_time
            self.total_icmp_count = 0
            self.detected = False
