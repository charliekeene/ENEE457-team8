# Overview: This file contains code to detect a SYN-ACK Denial of Service Attack
# Primary Author: Graham Rogers
# Description: A SYN-ACK is a Denial of Service attack in which a large number of handshakes are initiated with a server
# without completion. The result is that the server must manage a large amount of these unfinished handshakes resulting in a
# large consumption of resources and therefore a denial of resources towards normal usage.

from scapy.all import TCP, IP
import time
import logging

logger = logging.getLogger("ids")
FORMAT = "%(created)f %(message)s"
logging.basicConfig(level=logging.INFO, format=FORMAT, filename="logs/ids.log")

class syn_flood_detect:
    def __init__(self, ip_threshold=1000, total_threshold=5000, window_size=5):
        # Thresholds
        self.IP_THRESHOLD = ip_threshold       # SYNs per IP per port
        self.TOTAL_THRESHOLD = total_threshold # Total SYNs across all IPs/ports
        self.WINDOW_SIZE = window_size         # Time window in seconds

        # State
        self.syn_counts = {}
        self.total_syn_count = 0
        self.last_check_time = time.time()
        self.detected = False

    def process_packet(self, packet):   
        # Check if the packet has TCP and IP layers
        if packet.haslayer(TCP) and packet.haslayer(IP):
        
            # Check if the packet has only the SYN flag set (no ACK)
            # 0x02 is the numeric value for the SYN flag
            if packet[TCP].flags == 0x02:
                self.total_syn_count += 1
            
                src_ip = packet[IP].src
                dport = packet[TCP].dport
                key = (src_ip, dport)
            
                # Increment the counter for the unique key (source IP, dest port)
                self.syn_counts[key] = self.syn_counts.get(key, 0) + 1
            
                # Detect SYN Flood (only one detection/report per window)
                # DoS Check
                if (self.syn_counts[key] > self.IP_THRESHOLD) and (self.detected == False):
                    logger.info(f"SYN Flood (DoS), {src_ip}, {dport}")
                    self.detected = True

                # DDoS Check
                if (self.total_syn_count > self.TOTAL_THRESHOLD) and (self.detected == False):
                    logger.info(f"SYN Flood (DDoS), n/a, {dport}")
                    self.detected = True

        current_time = time.time()
        # Check is window is finished and if so, reset system
        if (current_time - self.last_check_time) >= self.WINDOW_SIZE:
            self.syn_counts = {}
            self.last_check_time = current_time
            self.total_syn_count = 0
            self.detected = False