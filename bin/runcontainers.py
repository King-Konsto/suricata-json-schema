#!/usr/bin/python

import docker
import logging
import threading
import os
from signal import *
import sys
import time

nof_threads = 4
logging.basicConfig(level=logging.INFO)

f = []
for (dirpath, dirnames, filenames) in os.walk("../versions"):
    f.extend(dirnames)
    break


logging.info("versions: ", f)

client = docker.from_env()

do_stop = False
def work(versions):
    global do_stop
    while True:
        if do_stop:
            logging.info("stopping worker")
            break
        try:
            v = versions.pop()
            run_version(v)
        except IndexError:
            break

def run_version(sversion):
    config_path = os.path.realpath('../versions/%s/configs' % sversion)
    pcaps_path = os.path.realpath('../pcaps')
    logs_path = os.path.realpath('../versions/%s/logs' % sversion)
    rules_path = os.path.realpath('../rules')
    bin_path = os.path.realpath('./')
    volumes = {}
    volumes[config_path] = {'bind': '/configs', 'mode':'ro'}
    volumes[pcaps_path] = {'bind': '/pcaps', 'mode':'ro'}
    volumes[logs_path] = {'bind': '/logs', 'mode':'rw'}
    volumes[rules_path] = {'bind': '/rules', 'mode':'ro'}
    volumes[bin_path] = {'bind': '/mybin', 'mode':'ro'}

    entry_script = "/mybin/run.sh"

    cont = client.containers.create('satta/%s' % sversion,
                                    command="/bin/bash",
                                    tty=True,
                                    volumes=volumes)
    cont.start()
    val, log = cont.exec_run(entry_script, stderr=True, stdout=True, stream=True)
    for line in log:
        print(line)
    cont.stop()
    cont.remove()

def stop_containers(*args):
    global do_stop
    do_stop = True
    logging.info("stopped via sig, running containers: %s", client.containers.list())
    for c in client.containers.list():
        logging.info("stopping %s", c)
        try:
            c.stop()
        except docker.errors.NotFound:
            pass
    for t in threads:
        t.join()
    logging.info("stopping done")
    sys.exit(0)

for sig in (SIGABRT, SIGILL, SIGINT, SIGSEGV, SIGTERM):
    signal(sig, stop_containers)

threads = []
for i in range(nof_threads):
    t = threading.Thread(target=work, args=(f,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()
