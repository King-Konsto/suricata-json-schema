#!/bin/bash

for ver in `./get_releases.sh | grep -v "suricata-1"`; do docker pull satta/$ver;  done
