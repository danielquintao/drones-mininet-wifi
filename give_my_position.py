

import os
import argparse
import requests

MN_SERVER = "http://127.0.0.1:5000/give-position" # drones must be in root namespace, see comments in fanet.py when we do net.addStation

parser = argparse.ArgumentParser(
    prog="give_my_position", 
    description="asks main mininet process to give position of the drone/node that called this program."
)
parser.add_argument("node")

args = parser.parse_args()

r = requests.get(MN_SERVER, params={"node": args.node})
if r.status_code != 200:
    print("\033[93mRequest to %s responded with status %s -> unable to change direction\033[0m" % (MN_SERVER, r.status_code))
else:
    print("\033[92mMy position: %s\033[0m" % (r.json()["position"]))
