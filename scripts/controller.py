import requests
import time
import logging
import random

logger = logging.getLogger("__name__")
FORMAT = "%(created)f %(message)s"
logging.basicConfig(level=logging.INFO, format=FORMAT, filename="logs/controller.log")

scripts = ["syn_flood.py", "fingerprint_attack.py", "icmp_attack.py"]
hosts = ["actor1", "actor2", "actor3", "amazon_alexa", "phillips_hue", "somfy"]
time.sleep(15)
while(True):
    host = random.choice(hosts)
    script = random.choice(scripts)


    print(f"[*] Sending '{script}' to {host}")
    try:
        r = requests.post(f"http://{host}_control:8000/run-script?script={script}")
        print(r.json())
    except Exception as e:
        print(f"[!] Error sending to {host}: {e}")
    print("Cycle complete.\n")
    match(script):
        case "syn_flood.py":
            logger.info(f"SYN Flood (DDoS) attack by {host}")
        case "fingerprint_attack.py":
            logger.info(f"Fingerprint violation attack by {host}")
        case "icmp_attack.py":
            logger.info(f"ICMP attack by {host}")

    time.sleep(random.randint(30,90))
    