from scapy.all import IP, TCP, UDP, ICMP, ARP
import json
import logging
import time

logger = logging.getLogger("ids")
FORMAT = "%(created)f %(message)s"
logging.basicConfig(level=logging.INFO, format=FORMAT, filename="logs/ids.log")

class Fingerprint:
    def __init__(self, config_path):
        with open(config_path) as f:
            config = json.load(f)

        self.violations = []

        self.allowed_ports = set(config.get("allowed_ports", []))
        self.min_size = config["packet_size"]["min_bytes"]
        self.max_size = config["packet_size"]["max_bytes"]
        self.allowed_protocols = set(config.get("allowed_protocols", []))
        self.disallowed_ips = set(config.get("disallowed_ips", []))

        self.WINDOW_SIZE = 5  # seconds
        self.last_check_time = time.time()

        self.detect_min_size = False
        self.detect_max_size = False
        self.detect_protocol = False
        self.detect_port = False
        self.detect_ip = False

    def process_packet(self, packet):
        
        size = len(packet)
        protoccol = "OTHER"
        src = dst = None
        sport = dport = None
        ttl = None

        # *** EXTRACT PACKET INFO ***
        if IP in packet:
            src = packet[IP].src
            dst = packet[IP].dst
            ttl = packet[IP].ttl
            protoccol = "IP"

            if TCP in packet:
                protoccol = "TCP"
                sport = packet[TCP].sport
                dport = packet[TCP].dport

                if dport == 22:
                    protoccol = "SSH"
            elif UDP in packet:
                protoccol = "UDP"
                sport = packet[UDP].sport
                dport = packet[UDP].dport
            elif ICMP in packet:
                protoccol = "ICMP"
        elif ARP in packet:
            protoccol = "ARP"
            src = packet[ARP].psrc
            dst = packet[ARP].pdst

        # *** CHECK AGAINST RULES ***
        if size < self.min_size and self.detect_min_size == False:
            self.violations.append(f"Packet too small ({size} bytes)")
            self.detect_min_size = True

        # check max size
        if size > self.max_size and self.detect_max_size == False:
            self.violations.append(f"Packet too large ({size} bytes)")
            self.detect_max_size = True

        # check protocol
        if self.allowed_protocols and protoccol not in self.allowed_protocols and self.detect_protocol == False:
            self.violations.append(f"Disallowed protoccol: {protoccol}")
            self.detect_protocol = True

        # check ports
        if self.allowed_ports:
            if dport and dport not in self.allowed_ports and self.detect_port == False:
                self.violations.append(f"Port violation: {sport}->{dport}")
                self.detect_port = True

        # check IPs
        if self.disallowed_ips and src in self.disallowed_ips and self.detect_ip == False:
            self.violations.append(f"Disallowed IP: {src}->{dst}")
            self.detect_ip = True

        # *** LOG VIOLATIONS AT THE END OF THE WINDOW ***
        current_time = time.time()
        # Check is window is finished and if so, reset system
        if (current_time - self.last_check_time) >= self.WINDOW_SIZE:
            if self.violations:
                violations_str = ";".join(self.violations)
                logger.info(f"{violations_str}, {src}, {dport},")
                # log(f"{violations_str}, {src}, {dport},")

            self.violations = []

            self.last_check_time = current_time
            self.detect_min_size = False
            self.detect_max_size = False
            self.detect_protocol = False
            self.detect_port = False
            self.detect_ip = False
