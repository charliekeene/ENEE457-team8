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
- actor1-3: randomized behavior communicating with ping, http to internet, tcp, udp, icmp random bytes to other hosts
- amazon_alexa, phillips_hue, somfy: based on real pcaps from IoT-23. See citation below.

Feature Overview
- SYN Attack Detection: Detect if too many SYN packets are received on the same port in a given time window (typically indicative of a DOS attack)
- ICMP Attack Detection: Detect if there are too many ICMP Type 8 packets being received in a given time window (typically indicative of a DoS/DDoS attack)

Citations  
[1] Sebastian Garcia, Agustin Parmisano, & Maria Jose Erquiaga. (2020). IoT-23: A labeled dataset with malicious and benign IoT network traffic (Version 1.0.0) [Data set]. Zenodo. http://doi.org/10.5281/zenodo.4743746
