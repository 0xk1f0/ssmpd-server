#FROM debian:bullseye-slim
FROM alpine:edge

# update repos and get wget
#RUN apt update && \
#    apt install -y wget
RUN apk update && \
    apk add bash

# change workdir
WORKDIR /app

# install librespot
#RUN wget https://dtcooper.github.io/raspotify/raspotify-latest_amd64.deb
#RUN sudo apt install -y ./raspotify-latest_amd64.deb && apt install -fy
RUN apk add --no-cache -X http://dl-cdn.alpinelinux.org/alpine/edge/testing \
    librespot

# install snap server
#RUN wget https://github.com/badaix/snapcast/releases/download/v0.27.0/snapserver_0.27.0-1_amd64.deb
#RUN sudo apt install -y ./snapserver_0.27.0-1_amd64.deb && apt install -fy
RUN apk add snapcast-server

# install mpd
#RUN apt install -y mpd
RUN apk add mpd

# copy setup script
COPY src/entrypoint.sh .

# ports
EXPOSE 1705
EXPOSE 1704

CMD ["bash", "entrypoint.sh"]
