#!/bin/bash
set -e

git clone https://github.com/OISF/suricata.git
cd suricata
git checkout suricata-4.1.5
git clone https://github.com/OISF/libhtp.git
./autogen.sh
./configure --enable-hiredis --enable-geoip --enable-luajit --prefix=/usr/ --sysconfdir=/etc/ --localstatedir=/var/
make install-full
cp /usr/lib/libhtp.so.2.0.0 /usr/lib/x86_64-linux-gnu/libhtp.so.2
ldconfig
