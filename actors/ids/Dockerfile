FROM python:3.10-alpine
COPY requirements.txt requirements.txt
COPY entrypoint.sh /entrypoint.sh
RUN apk add --no-cache libpcap-dev build-base
RUN pip install -r requirements.txt
ENTRYPOINT [ "/entrypoint.sh" ]