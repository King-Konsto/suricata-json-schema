#!/bin/bash

for ver in `./get_releases.sh`; do mkdir ../versions/$ver; mkdir ../versions/$ver/build; mkdir ../versions/$ver/logs; mkdir ../versions/$ver/schema; mkdir ../versions/$ver/configs; cp ./build.sh.in ../versions/$ver/build/build-$ver.sh; sed -i "s/suricata_version/$ver/" ../versions/$ver/build/build-$ver.sh; chmod +x ../versions/$ver/build/build-$ver.sh;  done
