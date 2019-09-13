#!/bin/bash

if suricata -V | fgrep " 4.1";then
  suricata -r /pcaps -c /configs/suricata.yaml -l /logs/ -k none
else
  for pcap in `find /pcaps -type f -name '*.pcap*'`; do
    echo "$pcap"
    suricata -r $pcap -c /configs/suricata.yaml -l /logs/ -k none
  done
fi
