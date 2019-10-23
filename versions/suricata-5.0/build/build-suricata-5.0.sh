#!/bin/bash
set -e

apt-get install libmaxminddb-dev -y
git clone https://github.com/OISF/suricata.git
cd suricata
git checkout suricata-5.0.0
git clone https://github.com/OISF/libhtp.git
./autogen.sh
./configure --enable-hiredis --enable-geoip --enable-luajit --prefix=/usr/ --sysconfdir=/etc/ --localstatedir=/var/
make install
make install-conf
cp /usr/lib/libhtp.so.2.0.0 /usr/lib/x86_64-linux-gnu/libhtp.so.2
ldconfig
