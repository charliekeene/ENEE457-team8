import time, requests, random

while True:
    url = "https://httpbin.org/get"
    print("Sending GET request to ", url)
    r = requests.get(url = url)

    time.sleep(random.randint(30, 90))
