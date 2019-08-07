#!/bin/bash

 curl --silent "https://api.github.com/repos/oisf/suricata/tags?page=1&per_page=100" | jq " .[] | .name" | sort | egrep -iv 'RC|beta' | sed 's/"//g' | grep -v "suricata-1"
