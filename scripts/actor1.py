from scapy.all import IP, ICMP, sr1
import time

while True:
    target = "actor2_sim" # Replace with your target IP
    print("Pinging", target)
    reply = sr1(IP(dst=target)/ICMP(type=8), timeout=3, verbose=0)

    time.sleep(10)