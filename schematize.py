#!/usr/bin/env python3

import datetime
import json
import os
import re
import sys
import jinja2

def process_level(fields, k1, v1, version):
    if "properties" in v1:
        for k2, v2 in v1["properties"].items():
            #print(k1, v2)
            dot = "."
            if len(k1) == 0:
                dot = ""
            process_level(fields, "%s%s%s" % (k1,dot,k2), v2, version)
    else:
        if not (k1 in fields):
            fields[k1] = {}
        if not "first_version" in fields[k1]:
            fields[k1]["first_version"] = version
        fields[k1]["last_version"] = version
        if "type" in v1:
            fields[k1]["type"] = v1["type"]
        else:
            fields[k1]["type"] = v1

def sort_ver(v):
    m = re.search(r'suricata-([0-9.]+)', v)
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
files = sorted(files, key=sort_ver)

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

# Render skeleton page to file
templateLoader = jinja2.FileSystemLoader(searchpath="./")
templateEnv = jinja2.Environment(loader=templateLoader)
template = templateEnv.get_template("field_details.rst.j2")
for k, v in fields.items():
    with open("output/%s.rst" % k, "w") as f:
        f.write(template.render(field_name=k,
                                field_type=v["type"],
                                field_first_seen_ver=v["first_version"],
                                field_last_seen_ver=v["last_version"],
                                date_generated=datetime.datetime.now()))