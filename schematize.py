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

# merge deltas
cleaned = []
for k, v in fields.items():
    if "_delta" in k:
        nonDelta = k.replace("_delta", "")
        if nonDelta in fields:
            fields[nonDelta]["has_delta"] = True
            cleaned.append(k)
for c in cleaned:
    del fields[c]


templateLoader = jinja2.FileSystemLoader(searchpath="./")
templateEnv = jinja2.Environment(loader=templateLoader)
template = templateEnv.get_template("field_details.rst.j2")
cntTemplate = templateEnv.get_template("field_content.rst.j2")
idxTemplate = templateEnv.get_template("index.rst.j2")
subidxTemplate = templateEnv.get_template("subindex.rst.j2")

toplevelPages = {}
lonePages = []
for k, v in fields.items():
    components = k.split(".")
    if len(components) > 1:
        if components[0] not in toplevelPages:
            toplevelPages[components[0]] = []
        toplevelPages[components[0]].append(k)
    else:
        lonePages.append(k)
    with open("output/%s.rst" % k, "w") as f:
        f.write(template.render(field_name=k,
                                field_line=('=' * len(k)),
                                field_type=v["type"],
                                field_first_seen_ver=v["first_version"],
                                field_last_seen_ver=v["last_version"],
                                has_delta=("has_delta" in v),
                                date_generated=datetime.datetime.now()))
    if not os.path.isfile("output/%s_content.rst.inc" % k):
        with open("output/%s_content.rst.inc" % k, "w") as f:
            f.write(cntTemplate.render(field_name=k,
                                    field_type=v["type"],
                                    field_first_seen_ver=v["first_version"],
                                    field_last_seen_ver=v["last_version"],
                                    has_delta=("has_delta" in v),
                                    date_generated=datetime.datetime.now()))

with open("output/index.rst", "w") as f:
    tops = list(toplevelPages.keys())
    all = tops + lonePages
    f.write(idxTemplate.render(toplevel_items=sorted(all)))

for k, v in toplevelPages.items():
    with open("output/%s.rst" % k, "w") as f:
        f.write(subidxTemplate.render(title=k,
                                      items=sorted(v)))