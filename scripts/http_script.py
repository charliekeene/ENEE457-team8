import time, requests

while True:
    url = "https://eolt9nnljpp9uau.m.pipedream.net"
    
    r = requests.get(url = url)

    data = r.json()

    print(data)

    time.sleep(30)
