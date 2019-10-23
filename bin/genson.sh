#!/bin/bash

for i in `find versions -name 'eve.json.gz'`; do
  echo $i
  zcat $i | genson -d newline -s seed.json > $i.schema
  zcat $i | jq .event_type | sort | uniq -c > $i.event_type_stats
  zcat $i | jq .app_proto | sort | uniq -c > $i.app_proto_stats
done