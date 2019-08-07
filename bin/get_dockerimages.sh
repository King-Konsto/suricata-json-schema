#!/bin/bash

for ver in `./get_releases.sh`; do docker pull satta/$ver;  done
