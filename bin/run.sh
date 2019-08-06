#!/bin/bash

mkdir -p /logs/suricata-2.0/
ls -Al /logs/suricata-2.0/
rm -v /logs/suricata-2.0/*
for pcap in `find /pcaps -type f -name '*.pcap*'`; do
  echo "$pcap"
  suricata -r $pcap -c /configs/suricata-2.0.yaml -S /rules/all.rules -l /logs/suricata-2.0;
done
