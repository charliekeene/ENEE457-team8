from scapy.all import IP, ICMP, sr1
import time
import random
import requests

hosts = ["actor1_sim", "actor2_sim", "zigbee_hub_sim"]
operations = ["ping", "http_get", "http_post" "_"]
get_url = "https://httpbin.org/get"
post_url = "https://httpbin.org/post"

while True:
    sleep_time = random.randint(5, 15)
    target = random.choice(hosts)
    operation = random.choice(operations)

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
        case "_":
            pass

    time.sleep(sleep_time)