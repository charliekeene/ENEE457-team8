from scapy.all import IP, ICMP, sr1
import time

while True:
    target = "enee457-team8-actor2-1" # Replace with your target IP
    print("Pinging", target)
    reply = sr1(IP(dst=target)/ICMP(type=8), timeout=3, verbose=0)

    time.sleep(10)
