from scapy.all import sniff, IP, TCP, UDP, ICMP, ARP
from collections import Counter
from globals import log
import json

class Fingerprint:
    def __init__(self, config_path):
        with open(config_path) as f:
            config = json.load(f)

        self.allowed_ports = set(config.get("allowed_ports", []))
        self.min_size = config["packet_size"]["min_bytes"]
        self.max_size = config["packet_size"]["max_bytes"]
        self.allowed_protocols = set(config.get("allowed_protocols", []))
        self.disallowed_ips = set(config.get("disallowed_ips", []))

    def process_packet(self, packet):
        violations = []
        
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
        if size < self.min_size:
            violations.append(f"Packet too small ({size} bytes)")

        # check max size
        if size > self.max_size:
            violations.append(f"Packet too large ({size} bytes)")

        # check protocol
        if self.allowed_protocols and protoccol not in self.allowed_protocols:
            violations.append(f"Disallowed protoccol: {protoccol}")

        # check ports
        if self.allowed_ports:
            if dport and dport not in self.allowed_ports:
                violations.append(f"Port violation: {sport}->{dport}")

        # check IPs
        if self.disallowed_ips and src in self.disallowed_ips:
            violations.append(f"Disallowed IP: {src}->{dst}")

        # *** LOG VIOLATIONS ***
        if violations:
            violations_str = ";".join(violations)
            log(f"{violations_str}, {src}, {dport},")
