#!/usr/bin/python

import docker
import logging
import threading
import os

f = []
for (dirpath, dirnames, filenames) in os.walk("./versions"):
    f.extend(dirnames)
    break

nof_threads = 2
logging.info(f)

client = docker.from_env()

def work(versions):
    while True:
        try:
            v = versions.pop()
            run_version(v)
        except IndexError:
            break
        print(v)

def run_version(sversion):
    config_path = os.path.realpath('./versions/%s/configs' % sversion)
    pcaps_path = os.path.realpath('./pcaps')
    logs_path = os.path.realpath('./versions/%s/logs' % sversion)
    rules_path = os.path.realpath('./rules')
    bin_path = os.path.realpath('./bin')
    volumes = {}
    volumes[config_path] = {'bind': '/configs', 'mode':'ro'}
    volumes[pcaps_path] = {'bind': '/pcaps', 'mode':'ro'}
    volumes[logs_path] = {'bind': '/logs', 'mode':'rw'}
    volumes[rules_path] = {'bind': '/rules', 'mode':'ro'}
    volumes[bin_path] = {'bind': '/mybin', 'mode':'ro'}
    
    cont = client.containers.create('satta/%s' % sversion,
                                    command="/bin/bash",
                                    tty=True,
                                    stdin_open=True,
                                    volumes=volumes)
    cont.start()
    log = cont.exec_run("/mybin/run.sh", stderr=True, stdout=True)
    for line in log:
            print(line)
    cont.stop()
    cont.remove()

threads = []
for i in range(nof_threads):
    t = threading.Thread(target=work, args=(f,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()