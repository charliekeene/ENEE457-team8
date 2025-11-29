import subprocess
import re

result = subprocess.run(
        ["ip", "-o", "addr", "show"],
        capture_output=True,
        text=True
    )

iface=""
ip =""

for line in result.stdout.splitlines():
    # Example line: "3: eth0    inet 172.17.0.2/16 ..."
    match = re.search(r'\d+:\s+(\S+)\s+.*inet\s+(\d+\.29\.\d+\.\d+)/', line)
    if match:
        iface, ip = match.groups()

subprocess.run(f"tcprewrite --infile=/pcaps/phillips_hue.pcap --outfile=/modified_pcaps/phillips_hue.pcap --srcipmap=192.168.1.132:{ip} --dstipmap=192.168.1.1:172.29.0.1", shell=True)
subprocess.run(f"tcpreplay --intf1={iface} /modified_pcaps/phillips_hue.pcap --loop=0 --mbps=10", shell=True)