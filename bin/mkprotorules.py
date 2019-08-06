#!/usr/bin/python

import sys
import re

protos = []

for line in sys.stdin:
    for proto in re.split('\s+', line.strip()):
        protos.append(proto)

i = 101;

for proto in protos:
    print("alert %s any any -> any any (msg:\"FOO %s\"; sid:%d;)" % (proto, proto.upper(), i))
    i += 1
