import os
import socket
import subprocess
import sys
import threading
import time
import requests
import random
import json

# Create a shared flag and a lock

connected_nodes = []
TOTAL_NODES = 9
EPS = 0.05
VOTATION_TIMEOUT = 8
VOTE_PROB = 0.6
target = [0,0,0]
votes = []
return_flag = False
votation_clock_expired = False
votation_ended = False


def get_ip(node_name):
    #I want to run ifconfig node_name command and get the ip address
    ifconfig_output = subprocess.check_output(["ifconfig", node_name]).decode("utf-8")
    for line in ifconfig_output.split("\n"):
        if "inet " in line:
            return line.split()[1]
    return None

def handle_node(node_socket, node_address, node_lost_in_votation):
    first_message_sent = False
    second_message_sent = False
    third_message_sent = False
    finished = False
    node_name = None
    while True:
        # Send commands to follower
        if len(connected_nodes) == TOTAL_NODES - 1 and not first_message_sent:
            command = "move to p2"
            node_socket.send(command.encode())
            first_message_sent = True
            
            while True:
                message = node_socket.recv(1024)
                if message == "":
                    connected_nodes.remove(node_address)
                    return
                arrival_msg = message[5:12]
                if arrival_msg != "arrived":
                    if message[0:2] == "OK":
                        command = "OK-master-received"
                        #send OK to node
                        node_socket.send(command.encode())
                    else:
                        print(message)
                else:
                    print(message)
                    command = "vote"
                    node_socket.send(command.encode())
                    break
        if first_message_sent and not second_message_sent:
            message = node_socket.recv(1024)
            vote = message[5:]
            node_name = message[:4]
            print(message)
            if vote == "OK":
                votes.append(1)
            else:
                votes.append(0)
            # wait for all votes
            while True:
                if node_name == node_lost_in_votation:
                    print("**losing connection with %s** (de proposito)" % (node_name,))
                    exit()  # simulate lost connection
                if votation_ended:
                    oks = votes.count(1)
                    if oks > len(votes)/2:
                        command = "return"
                        third_message_sent = True
                    else:
                        command = "move to p3"
                    node_socket.send(command.encode())
                    second_message_sent = True
                    break
        if first_message_sent and second_message_sent and not third_message_sent:
            # wait for arrival
            while True:
                message = node_socket.recv(1024)
                if message == "":
                    connected_nodes.remove(node_address)
                    return
                node_name = message[0:4]
                arrival_msg = message[5:12]
                if arrival_msg != "arrived":
                    if message[0:2] == "OK":
                        command = "OK-master-received"
                        #send OK to node
                        node_socket.send(command.encode())
                    else:
                        print(message)
                else:
                    print(message)
                    command = "return"
                    node_socket.send(command.encode())
                    third_message_sent = True
                    break
        if first_message_sent and second_message_sent and third_message_sent and not finished:
            # wait for arrival
            while True:
                message = node_socket.recv(1024)
                if message == "":
                    connected_nodes.remove(node_address)
                    return
                node_name = message[0:4]
                arrival_msg = message[5:12]
                if arrival_msg != "arrived":
                    if message[0:2] == "OK":
                        # print(str(message[2:])+ ": returning to p1")
                        command = "OK-master-received"
                        #send OK to node
                        node_socket.send(command.encode())
                    else:
                        print(message)  
                else:
                    print(message)
                    finished = True
                    break

def handle_master_as_node(myname):
    global target
    first_message_sent = False
    second_message_sent = False
    third_message_sent = False
    arrived = False
    global votation_clock_expired
    global votation_ended
    votation_clock = None
    while True:
        r = requests.get("http://127.0.0.1:5000/give-position", params={"node": myname})
        pos = r.json()["position"]
        dist2 = (pos[0] - target[0])**2 + (pos[1] - target[1])**2
        if dist2 < EPS and not arrived:
            print("Master: arrived")
            arrived = True
            if first_message_sent and not second_message_sent and votation_clock is None:
                # start votation clock when master arrives at place of votation
                print("Starting votation clock")
                votation_clock = time.time()

        if len(connected_nodes) == TOTAL_NODES - 1 and not first_message_sent:
            os.system("python change_my_dir.py " + myname + " 50 50")
            first_message_sent = True
            target = [50,50,0]
            arrived = False
        if first_message_sent and not second_message_sent and not votation_clock_expired:
            # votation clock expired!
            if votation_clock is not None and time.time() - votation_clock > VOTATION_TIMEOUT: 
                votation_clock_expired = True
                print("Votation clock expired!")
        if first_message_sent and not second_message_sent and (len(votes) == TOTAL_NODES - 1 or votation_clock_expired):
            # time for master to vote
            # (master is very polite, it waited for the other drones to vote first)
            vote_yes = random.random() < VOTE_PROB
            if vote_yes:
                votes.append(1)
                print("Master vote:  yes")
            if not vote_yes:
                votes.append(0)
                print("Master vote:  no")
            votation_ended = True
            second_message_sent = True
            oks = votes.count(1)
            arrived = False
            if oks > len(votes)/2:
                os.system("python change_my_dir.py " + myname + " 20 20")
                target = [20, 20, 0]
                print("Decision: Return")
            else:
                os.system("python change_my_dir.py " + myname + " 70 70")
                target = [70, 70, 0]
                print("Decision: Go to P3")
        if first_message_sent and second_message_sent and not third_message_sent:
            if arrived:
                time.sleep(1)
                os.system("python change_my_dir.py " + myname + " 20 20")
                target = [20, 20, 0]
                arrived = False
                third_message_sent = True
                print("Returning")

def handle_connections(master_socket, node_lost_in_votation):
    while True:
        # Accept incoming connections from slaves
        node_socket, node_address = master_socket.accept()
        print("Node connected from " + str(node_address))
        connected_nodes.append(node_address)

        # Create a thread to handle communication with the slave
        slave_thread = threading.Thread(target=handle_node, args=(node_socket, node_address, node_lost_in_votation))
        slave_thread.start()

def main():
    global return_flag
    global VOTATION_TIMEOUT
    global VOTE_PROB
    # Set the master's IP address and port
    master_port = 12345
    myname = sys.argv[1]
    my_ip = get_ip(myname+ "-wlan0")

    # read config
    with open("drones_config.json", "r") as f:
        config = json.load(f)
        VOTATION_TIMEOUT = config["VOTATION_TIMEOUT"]
        VOTE_PROB = config["VOTE_PROB"]

    node_lost_in_votation = raw_input("If you want to simulate a node losing communication during votation, type its name here, or just leave empty ")

    # Create a socket for the master
    master_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    master_socket.bind((my_ip, master_port))
    master_socket.listen(8)

    print("Master is listening on " + my_ip + ":" + str(master_port))
    master_node_thread = threading.Thread(target=handle_master_as_node, args=(myname,))
    master_node_thread.start()
    
    master_connections_thread = threading.Thread(target=handle_connections, args=(master_socket, node_lost_in_votation))
    master_connections_thread.start()

    
if __name__ == '__main__':
    main()
