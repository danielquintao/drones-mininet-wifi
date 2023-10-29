import socket
import os
import subprocess
import sys
import threading



def get_ip(node_name):
    #I want to run ifconfig node_name command and get the ip address
    ifconfig_output = subprocess.check_output(["ifconfig", node_name]).decode("utf-8")
    for line in ifconfig_output.split("\n"):
        if "inet " in line:
            return line.split()[1]
    return None

def handle_communication():
    node_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    node_socket.connect((master_ip, server_port))
    print("Conexao estabelecida")

    while True:
        data = node_socket.recv(1024)
        if not data:
            break
        if (data == "move"):
            #call change_my_dir.py in terminal
            os.system("python change_my_dir.py " + myname + " 50 50")
            reply = myname + "going to 50 50"
            node_socket.send(reply)
    node_socket.close()



master_name = sys.argv[1]
myname = sys.argv[2]
master_ip = get_ip(master_name+"-wlan0")
my_ip = get_ip(myname+ "-wlan0")
server_port = 12345


comm_thread = threading.Thread(target=handle_communication)
comm_thread.start()


