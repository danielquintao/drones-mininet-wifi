import socket
import os
import subprocess
import sys
import threading
import time
import requests
import random

target = [0,0,0]
EPS = 0.05
arrived = False
start_move = False
voting_state = False
comunication = True
go_to_safe_zone = False
in_p3 = False
TIMEOUT=6
VOTE_PROB = 0.1
drones = {
    "sta1": ((20.0, 20.0), (50.0, 50.0), (70.0, 70.0)),
    "sta2": ((10.0, 20.0), (40.0, 50.0), (60.0, 70.0)),
    "sta3": ((20.0, 10.0), (50.0, 40.0), (70.0, 60.0)),
    "sta4": ((10.0, 10.0), (40.0, 40.0), (60.0, 60.0)),
    "sta5": ((30.0, 30.0), (60.0, 60.0), (80.0, 80.0)),
    "sta6": ((30.0, 10.0), (60.0, 40.0), (80.0, 60.0)),
    "sta7": ((10.0, 30.0), (40.0, 60.0), (60.0, 80.0)),
    "sta8": ((20.0, 30.0), (50.0, 60.0), (70.0, 80.0)),
    "sta9": ((30.0, 20.0), (60.0, 50.0), (80.0, 70.0))
}

safe_zone = {
    "zone1": (50.0, 20.0),
    "zone2": (85.0, 55.0),
    "zone3": (15.0, 65.0),
}

def get_ip(node_name):
    #I want to run ifconfig node_name command and get the ip address
    ifconfig_output = subprocess.check_output(["ifconfig", node_name]).decode("utf-8")
    for line in ifconfig_output.split("\n"):
        if "inet " in line:
            return line.split()[1]
    return None

def give_the_shorter_safe_zone(pos):
    #calculate the distance between the drone and the safe zone
    #return the safe zone with the shortest distance
    shorter_zone="zone"
    actual_dist=1000000
    for i in range(3):
        zone = "zone" + str(i+1)
        x = safe_zone[zone][0]
        y = safe_zone[zone][1]
        dist = (pos[0] - x)**2 + (pos[1] - y)**2
        if dist < actual_dist:
            actual_dist = dist
            shorter_zone = zone
    return shorter_zone
        
    

def handle_communication():
    global target, arrived, voting_state, start_move,go_to_safe_zone, comunication, in_p3
    while go_to_safe_zone==False:
        if voting_state:
            node_socket.settimeout(2*TIMEOUT)  # wait longer during votation because other followers may delay votation result
        else:
            node_socket.settimeout(TIMEOUT)
        try:
            data = node_socket.recv(1024)
            if (data == ""):
                comunication = False
                raise socket.timeout
                
            if (data == "move to p2"):
                voting_state=False
                start_move=True
                target = drones[myname][1]
                arrived = False
                #call change_my_dir.py in terminal
                os.system("python change_my_dir.py " + myname + " %s %s" % (target[1], target[0]))
                reply = myname + " going to p2"
                node_socket.send(reply)
            if (data == "vote"):
                #vote YES with 60% probability
                voting_state=True
                if (random.random() < VOTE_PROB):
                    reply = myname + " OK"
                else:
                    reply = myname + " NO"
                node_socket.send(reply) 
            if (data == "move to p3"):
                voting_state=False
                target = drones[myname][2]
                arrived = False
                #call change_my_dir.py in terminal
                os.system("python change_my_dir.py " + myname + " %s %s" % (target[1], target[0]))
                reply = myname + " going to p3"
                node_socket.send(reply)
            if (data == "return"):
                voting_state=False
                target = drones[myname][0]
                arrived = False
                in_p3 = False
                start_move = True
                #call change_my_dir.py in terminal
                os.system("python change_my_dir.py " + myname + " %s %s" % (target[1], target[0]))
                reply = myname + " returning"
                node_socket.send(reply)
        except:
            if start_move:
                print("timeout going to safe zone")
                go_to_safe_zone=True
                break
    node_socket.close()

def get_pos():
    global pos, arrived, target,voting_state,start_move, comunication,go_to_safe_zone, in_p3
    while go_to_safe_zone==False:
        r = requests.get("http://127.0.0.1:5000/give-position", params={"node": myname})
        pos = r.json()["position"]
        dist2 = (pos[0] - target[0])**2 + (pos[1] - target[1])**2
        if voting_state == False and start_move == True and comunication == True and in_p3 == False:
            node_socket.send("OK " + myname)
            time.sleep(1)
        if dist2 < EPS and not arrived:
            if target == drones[myname][2]:
                in_p3 = True
                start_move = False
            if target == drones[myname][0]:
                start_move = False
            node_socket.send(myname + " arrived at " + str(target))
            arrived = True
            
    if go_to_safe_zone==True:
        r = requests.get("http://127.0.0.1:5000/give-position", params={"node": myname})
        pos = r.json()["position"]
        zone = give_the_shorter_safe_zone(pos)
        target = safe_zone[zone]
        os.system("python change_my_dir.py " + myname + " %s %s" % (target[1], target[0]))  
        while True:
            r = requests.get("http://127.0.0.1:5000/give-position", params={"node": myname})
            pos = r.json()["position"]
            dist2 = (pos[0] - target[0])**2 + (pos[1] - target[1])**2
            if dist2 < EPS and not arrived:
                print("arrived in safe zone")
                arrived = True
                break
      
        

master_name = sys.argv[1]
myname = sys.argv[2]
master_ip = get_ip(master_name+"-wlan0")
my_ip = get_ip(myname+ "-wlan0")
server_port = 12345
node_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
node_socket.connect((master_ip, server_port))
print("Connection established")

comm_thread = threading.Thread(target=handle_communication)
comm_thread.start()

pos_thread = threading.Thread(target=get_pos)
pos_thread.start()

while True:
    x = raw_input("Type f to make node lose communication ")

    if x == 'f':
        comunication = False
        print("failing")
        break
