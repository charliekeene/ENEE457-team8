import requests
import time

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