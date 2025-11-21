import time, requests

while True:
    url = "https://httpbin.org/get"
    print("Sending GET request to ", url)
    r = requests.get(url = url)

    time.sleep(30)
