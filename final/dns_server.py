#!/usr/bin/env python3

from socket import *
import sys

# Variables from command line
topo_dir = sys.argv[1]      # topology
log = sys.argv[2]           # write to here
server_port = sys.argv[3]   # UDP listen port
dec_method = sys.argv[4]    # "round-robin" or "lowest-latency"

server_socket = socket(AF_INET, SOCK_DGRAM)

HOST = "127.0.0.1"
server_socket.bind((HOST , server_port))

# Recieving message from client
client_message, client_address = server_socket.recvfrom(2048)


print("Received Message from Client: ", client_message.decode())

# Modifying the message
client_message = client_message.decode().upper()

print("Sending Message to Client: ", client_message)

# Sending the encoded modified message back to the client
server_socket.sendto(client_message.encode(), client_address)

server_socket.close()