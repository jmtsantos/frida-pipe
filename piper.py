import time
import frida
import os
import sys
import click
import logging
import argparse

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s",
                    datefmt='%m-%d/%H:%M:%S')

def get_all_process(device, pkgname):
    return [process for process in device.enumerate_processes() if pkgname in process.name]

def is_ascii(s):
    return len(s) == len(s.encode())

def on_message(message, data):
    try:
        if is_ascii(message['payload']) and message['payload'].isprintable() and len(message['payload'])>1:
            click.secho("[decoder] {}".format(message['payload'], fg='green'))
    except: 
        pass

# args
parser = argparse.ArgumentParser(prog='frida-pipe')
parser.add_argument('--script', required=True, type=str,
                    help='the script that is going to perform the decrypt')
args = parser.parse_args()

# get the process
device = frida.get_usb_device()
target = device.get_frontmost_application()

processes = get_all_process(device, target.identifier)

for process in processes:
    if target.pid is not None and process.pid != target.pid:
        continue

    logging.info("[piper]: found target [{}] {}".format(
        process.pid, process.name))

session = device.attach(process.pid)

with open(args.script) as f:
    script = session.create_script(f.read())

script.on('message', on_message)
script.load()

for line in sys.stdin:
    script.exports.decodeNative(line.replace("\n", ""))
