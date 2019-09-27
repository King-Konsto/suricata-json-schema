#!/usr/bin/env python3

import datetime
import json
import os
import re
import sys
import jinja2
import pprint

def process_level(fields, k1, v1, version):
    if "properties" in v1:
        for k2, v2 in v1["properties"].items():
            #print(k1, v2)
            dot = "."
            if len(k1) == 0:
                dot = ""
            process_level(fields, "%s%s%s" % (k1,dot,k2), v2, version)
    else:
        if not (version in fields):
            fields[version] = {}
        items = k1.split('.')
        if len(items) == 1:
            kk = "toplevel"
        else:
            if "_delta" in k1:
                kk = "stats-delta"
            else:
                kk = items[0]
        if not (kk in fields[version]):
            fields[version][kk] = 0
        fields[version][kk] = fields[version][kk] + 1

def sort_ver(v):
    m = re.search(r'([0-9.]+)', v)
    version = m.group(1)
    vers =  version.split('.')
    if len(vers) == 2:
        vers.append('0')
    return list(map(int, vers))


# Gather and sort input files by version.
files = []
for (dirpath, dirnames, filenames) in os.walk("versions"):
    for name in filenames:
        if "schema" in name:
            json_file = os.path.join(dirpath, name)
            files.append(json_file)

# Parse schemas and extract information.
fields = {}
for f in files:
    m = re.search(r'suricata-([0-9.]+)', f)
    version = m.group(1)
    try:
        data = json.load(open(f))
        process_level(fields, "", data, version)
    except Exception as inst:
        #print("Unexpected error:", inst)
        pass

topLevel = set()
for _, v in fields.items():
    for k, _ in v.items():
        topLevel.add(k)

print("version", end ="")
for tl in topLevel:
    print(",%s" % tl, end ="")
print()

versions = sorted(fields.keys(), key=sort_ver)


for version in versions:
    print(version, end ="")
    for tl in topLevel:
        if tl in fields[version]:
            print(",%d"% fields[version][tl], end ="")
        else:
            print(",0", end ="")
    print()
