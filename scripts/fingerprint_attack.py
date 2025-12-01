import json
import random
import os
from scapy.all import Ether, IP, TCP, UDP, Raw, wrpcap, send

hosts = ["actor2_sim", "actor3_sim", "phillips_hue_sim", "somfy_sim", "amazon_alexa_sim"]

class BadTrafficGenerator:
    def __init__(self, config_path):
        with open(config_path) as f:
            config = json.load(f)

        self.allowed_ports = set(config.get("allowed_ports", []))
        self.min_size = config["packet_size"]["min_bytes"]
        self.max_size = config["packet_size"]["max_bytes"]
        self.allowed_protocols = set(config.get("allowed_protocols", []))
        self.disallowed_ips = set(config.get("disallowed_ips", []))
    
    def random_ip(self):
        return ".".join(str(random.randint(1, 254)) for _ in range(4))

    def random_bad_port(self):
        p = random.randint(1, 65535)
        while p in self.allowed_ports:
            p = random.randint(1, 65535)
        return p

    def random_bad_protocol(self):
        bads = ["SMTP", "TELNET", "UNKNOWN", "FTP", "OTHER"]
        return random.choice(bads)

    def random_bad_size(self):
        if random.choice([True, False]):
            return random.randint(1, self.min_size - 1)
        else:
            return random.randint(self.max_size + 1, 5000)

    def generate_packet(self):
        violate_ip     = random.choice([True, False])
        violate_port   = random.choice([True, False])
        violate_proto  = random.choice([True, False])
        violate_size   = random.choice([True, False])


        if violate_ip:
            src_ip = random.choice(list(self.disallowed_ips))
        else:
            src_ip = self.random_ip()

        dst_ip = random.choice(hosts)

        if violate_port:
            dst_port = self.random_bad_port()
        else:
            dst_port = random.choice(list(self.allowed_ports))

        if violate_proto:
            proto = self.random_bad_protocol()
        else:
            proto = random.choice(["TCP", "UDP"])

        if violate_size:
            size = self.random_bad_size()
        else:
            size = random.randint(self.min_size, self.max_size)

        payload = os.urandom(size)

        if proto == "TCP":
            pkt = (
                Ether() /
                IP(src=src_ip, dst=dst_ip) /
                TCP(
                    sport=random.randint(1024, 65535),
                    dport=dst_port,
                    flags="S"
                ) /
                Raw(payload)
            )

        elif proto == "UDP":
            pkt = (
                Ether() /
                IP(src=src_ip, dst=dst_ip) /
                UDP(
                    sport=random.randint(1024, 65535),
                    dport=dst_port
                ) /
                Raw(payload)
            )

        else:
            pkt = (
                Ether() /
                IP(src=src_ip, dst=dst_ip, proto=255) /
                Raw(payload)
            )

        send(pkt, verbose=0)
        print(f"Sending malformed packet to {dst_ip}, {pkt.summary()}")

if __name__ == "__main__":
    gen = BadTrafficGenerator("scripts/fingerprint_rules.json")

    print("Generating bad traffic...")

    packets = [gen.generate_packet() for _ in range(50)]
