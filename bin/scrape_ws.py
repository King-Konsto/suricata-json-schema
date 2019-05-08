#!/usr/bin/python

from bs4 import BeautifulSoup
import re
import requests

base = "https://wiki.wireshark.org/SampleCaptures"

result = requests.get(base)
soup = BeautifulSoup(result.content, features="lxml")
for link in soup.findAll('a', href=re.compile(r"SampleCaptures.*target=.*\.pcap")):
    url = "http://wiki.wireshark.org" + link['href']
    filename = url.split("=")[-1]
    print("getting " + filename) 
    try:
        r = requests.get(url, allow_redirects=True)
        open(filename, 'wb').write(r.content)
    except requests.exceptions.ConnectionError as e:
        print(e)