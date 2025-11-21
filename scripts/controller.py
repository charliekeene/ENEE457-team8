import requests
import time

time.sleep(15)

host = "actor2"
script = "syn_flood.py"
print(f"[*] Sending '{script}' to {host}")
try:
    r = requests.post(f"http://enee457-team8-{host}-1:8000/run-script?script={script}", timeout=3)
    print(r.json())
except Exception as e:
    print(f"[!] Error sending to {host}: {e}")
print("Cycle complete.\n")