FROM python:3.10-alpine

# Install relevant libraries needed by python tool
RUN apk update && \
    apk add --no-cache libpcap-dev tcpdump build-base python3-dev linux-headers && \
    rm -rf /var/cache/apk/*

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt