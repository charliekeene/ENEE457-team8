# ENEE457-team8
Docker install instructions [here](https://docs.docker.com/engine/install/)  

HTTP dashboard [here](https://pipedream.com/@magneticsocks20/projects/proj_YRsD6L3/p_V9CpYqN/inspect), endpoint url is https://eolt9nnljpp9uau.m.pipedream.net

Run using
```bash
    docker compose up -d
```

Containers will need a rebuild after changing Dockerfile. Use
```bash
    docker compose up -d --force-recreate --build
```

Examine containers using
```bash
    docker ps -a
```

Start shell in container using
```bash
    docker exec -it <container_name> sh
```

Network Overview
- actor1: Sends pings to actor2 every 3 seconds
- actor2: Nothing yet
- zigbee_hub: Hub for zigbee network, modeled after Phillips Hue Bridge. Currently sends HTTP GET every 30 seconds
- test_app: Test app from docker compose quickstart

Feature Overview
- SYN Attack Detection: Detect if too many SYN packets are received on the same port in a given time window (typically indicative of a DOS attack)
- ICMP Attack Detection: Detect if there are too many ICMP Type 8 packets being received in a given time window (typically indicative of a DoS/DDoS attack)
