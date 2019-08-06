#!/bin/bash
set -e

git clone https://github.com/OISF/suricata.git
cd suricata
git checkout suricata-4.1.4
git clone https://github.com/OISF/libhtp.git
./autogen.sh
./configure --enable-hiredis --enable-geoip --enable-luajit --prefix=/usr/ --sysconfdir=/etc/ --localstatedir=/var/
make install-full
ldconfig