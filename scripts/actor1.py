from scapy.all import IP, ICMP, sr1
import time

while True:
    target = "enee457-team8-actor2-1" # Replace with your target IP
    print("Test")
    reply = sr1(IP(dst=target)/ICMP(type=8), timeout=3)
    reply.show()

    time.sleep(10)
