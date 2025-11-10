FROM python:3.10-alpine
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN apk update \
    && apk add --no-cache \
       --repository http://dl-cdn.alpinelinux.org/alpine/edge/testing \
       hping3 \
       libpcap \
    && rm -rf /var/cache/apk/*