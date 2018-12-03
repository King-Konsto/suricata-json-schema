FROM debian:buster

ARG suricata_version="suricata-4.1.0"

RUN echo "deb-src http://deb.debian.org/debian buster main" >> /etc/apt/sources.list

RUN echo "deb-src http://deb.debian.org/debian buster-updates main" >> /etc/apt/sources.list

RUN apt-get update && apt-get dist-upgrade -y && apt-get build-dep suricata -y

RUN apt-get -y install libnetfilter-queue-dev liblz4-dev rustc cargo git python3-pip

RUN pip3 install genson

RUN git clone https://github.com/OISF/suricata.git && cd suricata && git checkout ${suricata_version}

RUN cd suricata && git clone https://github.com/OISF/libhtp.git

RUN cd suricata && ./autogen.sh && ./configure --enable-hiredis --enable-geoip --enable-luajit --prefix=/usr/ --sysconfdir=/etc/ --localstatedir=/var/ && make install-full && ldconfig

COPY configs/${suricata_version}.yaml /etc/suricata/suricata.yaml

RUN suricata --build-info
