from scapy.all import IP, ICMP, TCP, UDP, sr1, send
import time
import random
import requests
import os

hosts = ["actor1_sim", "actor3_sim", "phillips_hue_sim", "somfy_sim", "amazon_alexa_sim"]
operations = ["ping", "http_get", "http_post", "tcp", "udp", "icmp", "_"]
get_url = "https://httpbin.org/get"
post_url = "https://httpbin.org/post"

while True:
    sleep_time = random.randint(5, 15)
    target = random.choice(hosts)
    operation = random.choice(operations)

    payload = os.urandom(random.randint(20, 140))

    match operation:
        case "ping":
            print("Pinging", target)
            reply = sr1(IP(dst=target)/ICMP(type=8), timeout=3, verbose=0)
        case "http_get":
            print("Sending GET request to ", get_url)
            r = requests.get(url = get_url)
        case "http_post":
            print("Sending POST request to ", post_url)
            r = requests.post(url = post_url, data = {'temp': '22C', 'humidity': '45%'})
        case "tcp":
            print("Sending TCP packet to", target)
            dst_port = random.randint(1024, 65535)
            src_port = random.randint(1024, 65535)
            packet = IP(dst=target)/TCP(sport=src_port, dport=dst_port)/payload
            send(packet, verbose=0)
        case "udp":
            print("Sending UDP packet to", target)
            dst_port = random.randint(1024, 65535)
            packet = IP(dst=target)/UDP(dport=dst_port)/payload
            send(packet, verbose=0)
        case "icmp":
            print("Sending ICMP packet to", target)
            packet = IP(dst=target)/ICMP()/payload
            send(packet, verbose=0)
        case "_":
            pass

    time.sleep(sleep_time)