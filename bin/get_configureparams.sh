#!/bin/bash

for ver in `./get_releases.sh`; do docker run satta/$ver /suricata/configure --help > ../versions/$ver/build/configurehelp.txt;  done
