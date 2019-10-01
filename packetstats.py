#!/usr/bin/env python3

# this needs tcpdstat output as input

import sys
import re
import pprint

total_match = re.compile('\[[0]\] total +(\d+)')
l2_match = re.compile('\[[2]\] +([^ ]+) +(\d+)')
l3_match = re.compile('\[[3]\] +([^ ]+) +(\d+)')

total_count = 0
l2_props = {}
l3_props = {}

with open(sys.argv[1]) as fp:
   line = fp.readline()
   while line:
       m = total_match.match(line)
       if m:
           total_count += int(m.group(1))
       m = l2_match.match(line)
       if m:
           proto = m.group(1)
           if proto not in l2_props:
               l2_props[proto] = 0
           l2_props[proto] += int(m.group(2))
       m = l3_match.match(line)
       if m:
           proto = m.group(1)
           if proto not in l3_props:
               l3_props[proto] = 0
           l3_props[proto] += int(m.group(2))
       line = fp.readline()

sorted_l2_props = sorted(l2_props.items(), key=lambda kv: kv[1])
for proto, val in sorted_l2_props:
    print(proto, val, round((val/total_count)*10000)/100 )

print("===================")

sorted_l3_props = sorted(l3_props.items(), key=lambda kv: kv[1])
for proto, val in sorted_l3_props:
    print(proto, val, round((val/total_count)*10000)/100 )