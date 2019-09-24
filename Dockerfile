FROM debian:buster

RUN echo "deb-src http://deb.debian.org/debian buster main" >> /etc/apt/sources.list

RUN echo "deb-src http://deb.debian.org/debian buster-updates main" >> /etc/apt/sources.list

RUN apt-get update && apt-get dist-upgrade -y && apt-get build-dep suricata -y

RUN apt-get -y install libnetfilter-queue-dev liblz4-dev rustc cargo git python3-pip wget tar tcpdump tcpreplay jq

RUN pip3 install genson

ARG suricata_version="suricata-4.1.4"

COPY versions/suricata-${suricata_version}/build/build-suricata-${suricata_version}.sh /usr/local/bin/build.sh

RUN /usr/local/bin/build.sh

COPY versions/suricata-${suricata_version}/configs/suricata.yaml /etc/suricata/suricata.yaml
