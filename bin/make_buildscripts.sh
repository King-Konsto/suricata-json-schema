#!/bin/bash

for ver in `./get_releases.sh`; do cp build/build.sh.in build/build-$ver.sh; sed -i "s/suricata_version/$ver/" build/build-$ver.sh; chmod +x build/build-$ver.sh;  done
