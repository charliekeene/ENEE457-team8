FROM python:3.10-alpine
COPY requirements.txt requirements.txt
COPY entrypoint.sh /entrypoint.sh
RUN pip install -r requirements.txt
# Install build deps
RUN apk add --no-cache \
    build-base \
    libpcap-dev \
    autoconf \
    automake \
    libtool \
    wget
# Build tcpreplay
RUN wget https://github.com/appneta/tcpreplay/releases/download/v4.4.4/tcpreplay-4.4.4.tar.gz && \
    tar xzf tcpreplay-4.4.4.tar.gz && \
    cd tcpreplay-4.4.4 && \
    ./configure && \
    make && \
    make install && \
    cd / && rm -rf tcpreplay-4.4.4*
RUN mkdir /modified_pcaps
ENTRYPOINT [ "/entrypoint.sh" ]