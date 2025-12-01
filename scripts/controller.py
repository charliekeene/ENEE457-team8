import requests
import time
import logging

logger = logging.getLogger("__name__")
FORMAT = "%(created)f %(message)s"
logging.basicConfig(level=logging.INFO, format=FORMAT, filename="logs/controller.log")

time.sleep(15)

host = "actor2"
script = "fingerprint_attack.py"

print(f"[*] Sending '{script}' to {host}")
try:
    r = requests.post(f"http://{host}_control:8000/run-script?script={script}")
    print(r.json())
except Exception as e:
    print(f"[!] Error sending to {host}: {e}")
print("Cycle complete.\n")
logger.info(f"Fingerprint violation attack by {host}")

time.sleep(27)

host = "phillips_hue"
script = "syn_flood.py"

print(f"[*] Sending '{script}' to {host}")
try:
    r = requests.post(f"http://{host}_control:8000/run-script?script={script}")
    print(r.json())
except Exception as e:
    print(f"[!] Error sending to {host}: {e}")
print("Cycle complete.\n")
logger.info(f"SYN Flood (DDoS) attack by {host}")