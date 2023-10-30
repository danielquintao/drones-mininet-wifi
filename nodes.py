import socket
import os
import subprocess
import sys
import threading
import time
import requests

target = [0,0,0]
EPS = 0.05
arrived = False

drones = {
    "sta1": ((20.0, 20.0), (50.0, 50.0), (70.0, 70.0)),
    "sta2": ((10.0, 20.0), (40.0, 50.0), (60.0, 70.0)),
    "sta3": ((20.0, 10.0), (50.0, 40.0), (70.0, 60.0)),
    "sta4": ((10.0, 10.0), (40.0, 40.0), (60.0, 60.0)),
    "sta5": ((30.0, 30.0), (60.0, 60.0), (80.0, 80.0)),
    "sta6": ((30.0, 10.0), (60.0, 40.0), (80.0, 60.0)),
    "sta7": ((10.0, 30.0), (40.0, 60.0), (60.0, 80.0)),
    "sta8": ((20.0, 30.0), (50.0, 60.0), (70.0, 70.0)),
    "sta9": ((30.0, 20.0), (60.0, 50.0), (80.0, 70.0))
}

def get_ip(node_name):
    #I want to run ifconfig node_name command and get the ip address
    ifconfig_output = subprocess.check_output(["ifconfig", node_name]).decode("utf-8")
    for line in ifconfig_output.split("\n"):
        if "inet " in line:
            return line.split()[1]
    return None

def handle_communication():
    global target, arrived
    while True:
        data = node_socket.recv(1024)
        if not data:
            break
        if (data == "move to p2"):
            target = drones[myname][1]
            arrived = False
            #call change_my_dir.py in terminal
            os.system("python change_my_dir.py " + myname + " %s %s" % (target[1], target[0]))
            reply = myname + " going to 50 50"
            node_socket.send(reply)
        if (data == "move to p3"):
            target = drones[myname][2]
            arrived = False
            #call change_my_dir.py in terminal
            os.system("python change_my_dir.py " + myname + " %s %s" % (target[1], target[0]))
            reply = myname + " going to 70 70"
            node_socket.send(reply)
        if (data == "return"):
            target = drones[myname][0]
            arrived = False
            #call change_my_dir.py in terminal
            os.system("python change_my_dir.py " + myname + " %s %s" % (target[1], target[0]))
            reply = myname + " going to 0 0"
            node_socket.send(reply)
    node_socket.close()

def get_pos():
    global pos, arrived, target
    while True:
        time.sleep(5)
        r = requests.get("http://127.0.0.1:5000/give-position", params={"node": myname})
        pos = r.json()["position"]
        dist2 = (pos[0] - target[0])**2 + (pos[1] - target[1])**2
        if dist2 < EPS and not arrived:
            node_socket.send("arrived")
            arrived = True

master_name = sys.argv[1]
myname = sys.argv[2]
master_ip = get_ip(master_name+"-wlan0")
my_ip = get_ip(myname+ "-wlan0")
server_port = 12345
node_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
node_socket.connect((master_ip, server_port))
print("Conexao estabelecida")

comm_thread = threading.Thread(target=handle_communication)
comm_thread.start()

pos_thread = threading.Thread(target=get_pos)
pos_thread.start()

while True:
    pic = raw_input()
    if pic == "y":
        node_socket.send("OK")
    if pic == "n":
        node_socket.send("NO")
       
