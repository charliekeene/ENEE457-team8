import time, requests

while True:
    url = "https://eolt9nnljpp9uau.m.pipedream.net"
    print("Sending GET request to ", url)
    r = requests.get(url = url)

    data = r.json()

    

    time.sleep(30)
