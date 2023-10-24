import socket
import os
import subprocess
import sys


def get_ip(node_name):
    #I want to run ifconfig node_name command and get the ip address
    ifconfig_output = subprocess.check_output(["ifconfig", node_name]).decode("utf-8")
    for line in ifconfig_output.split("\n"):
        if "inet " in line:
            return line.split()[1]
    return None

master_name = sys.argv[1]
myname = sys.argv[2]
master_ip = get_ip(master_name + "-wlan0")
my_ip = get_ip(myname + "-wlan0")
server_port = 12345

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((master_ip, server_port))
server_socket.listen(1)

print("Aguardando...", master_ip, ":", server_port)
connection, client_address = server_socket.accept()
print("Conexao estabelecida", client_address)

while True:
    data = connection.recv(1024)
    if not data:
        break
    if (data == b"move"):
        os.system("python change_my_dir.py sta2 1 1")
        
        

connection.close()
