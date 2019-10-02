#!/bin/bash

for pcap in `find /pcaps -type f -name '*.pcap*'`; do
  echo "$pcap"
  suricata -r $pcap -c /configs/suricata.yaml -l /logs/ -k none
done

echo "--simulate-ips with /pcaps/http_drop.pcap"
suricata -r /pcaps/http_drop.pcap -c /configs/suricata.yaml -l /logs/ -k none --simulate-ips
