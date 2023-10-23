"""Changes the direction of a drone

In Mininet-WiFi, the position of stations is managed by the
main process initiating the network, not by the station itself.

Therefore, our trick to allow a station to decide on its path
will be to send a request to the main process, which must update
the direction of the station itself.

In order to use this script, we must first set an environment variable
DRONENAME inside the drone/node, then we can call this script from it.
"""

import os
import argparse
import requests

MN_SERVER = "http://127.0.0.1:5000/update-direction" # drones must be in root namespace, see comments in fanet.py when we do net.addStation

parser = argparse.ArgumentParser(
    prog="change_my_dir", 
    description="asks main mininet process to change direction of the drone/node that called this program."
)
parser.add_argument("node")
parser.add_argument("latitude_dir", type=float)
parser.add_argument("longitude_dir", type=float)

args = parser.parse_args()

r = requests.get(MN_SERVER, params={"node": args.node, "latdir": args.latitude_dir, "longdir": args.longitude_dir})
if r.status_code != 200:
    print("\033[93mRequest to %s responded with status %s -> unable to change direction\033[0m" % (MN_SERVER, r.status_code))
