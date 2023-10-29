import os
import socket
import subprocess
import sys
import threading

# Create a shared flag and a lock

connected_nodes = []
TOTAL_NODES = 4



def get_ip(node_name):
    #I want to run ifconfig node_name command and get the ip address
    ifconfig_output = subprocess.check_output(["ifconfig", node_name]).decode("utf-8")
    for line in ifconfig_output.split("\n"):
        if "inet " in line:
            return line.split()[1]
    return None

def handle_node(node_socket, node_address):
    first_message_sent = False
    second_message_sent = False
    while True:
        # Receive commands from the master
        if len(connected_nodes) == TOTAL_NODES - 1 and not first_message_sent:
            command = "move"
            node_socket.send(command.encode())
            first_message_sent = True

            response = node_socket.recv(1024)
            print(str(node_address) + ":  " + str(response.decode()))

def handle_master_as_node(myname):
    first_message_sent = False
    second_message_sent = False
    while True:
        if len(connected_nodes) == TOTAL_NODES - 1 and not first_message_sent:
            print("ueue")
            print(myname)
            os.system("python change_my_dir.py " + myname + " 50 50")
            first_message_sent = True

def main():
    # Set the master's IP address and port
    master_port = 12345
    myname = sys.argv[1]
    my_ip = get_ip(myname+ "-wlan0")

    # Create a socket for the master
    master_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    master_socket.bind((my_ip, master_port))
    master_socket.listen(5)

    print("Master is listening on " + my_ip + ":" + str(master_port))
    master_node_thread = threading.Thread(target=handle_master_as_node, args=(myname,))
    master_node_thread.start()
    while True:
        # Accept incoming connections from slaves
        node_socket, node_address = master_socket.accept()
        print("Node connected from " + str(node_address))
        connected_nodes.append(node_address)

        # Create a thread to handle communication with the slave
        slave_thread = threading.Thread(target=handle_node, args=(node_socket, node_address))
        slave_thread.start()

        slave_thread = threading.Thread(target=handle_node, args=(node_socket, node_address))
        slave_thread.start()


    
if __name__ == '__main__':
    main()
