#!/usr/bin/env python3

from socket import *
import sys

# Variables from command line
topo_dir = sys.argv[1]      # topology
log = sys.argv[2]           # write to here
server_port = sys.argv[3]   # UDP listen port
dec_method = sys.argv[4]    # "round-robin" or "lowest-latency"

serverSocket = socket(AF_INET, SOCK_DGRAM)

HOST = "127.0.0.1"
serverSocket.bind((HOST , server_port))

# Recieving message from client
clientMessage, clientAddress = serverSocket.recvfrom(2048)


print("Received Message from Client: ", clientMessage.decode())

# Modifying the message
clientMessage = clientMessage.decode().upper()

print("Sending Message to Client: ", clientMessage)

# Sending the encoded modified message back to the client
serverSocket.sendto(clientMessage.encode(), clientAddress)

serverSocket.close()