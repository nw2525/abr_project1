#!/usr/bin/env python3.10

from socket import *
import requests
import sys
import threading
import time

assert len(sys.argv) == 5, "Error: Expected 4 arguments. Usage: ./proxy <log> <listen-port> <fake-ip> <server-ip>"

# Variables from command line
log = sys.argv[1]
listen_port = sys.argv[2]   # receive from client
fake_ip = sys.argv[3]       # 127.0.0.1
server_ip = sys.argv[4]     # 127.0.0.1
server_port = '80'   # send to server

file = open(log, "a")
# Set up proxy
proxy_socket = socket(AF_INET, SOCK_STREAM)
proxy_socket.bind((str(fake_ip), int(listen_port)))
proxy_socket.listen(1)

while True:
    # connect to client(s)
    client_socket, addr = proxy_socket.accept()

    # connect to server
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.connect((str(server_ip), int(server_port)))
    connected = True
    start = time.time()

    while connected:
        ### maybe check if still connected to client(s)/server
        client_request = client_socket.recv(10**5)
        server_socket.send(client_request)
        chunk_start = time.time()
        server_message = server_socket.recv(10**6)
        end = time.time()
        chunk_size = len(server_message)

        # Process chunk for log
        duration = end - chunk_start
        chunk_name = "foobar"

        output = str(end) + " " + str(duration) + " " + server_ip + " " + chunk_name + " " + str(chunk_size)
        print(output)
        file.write(output + "\n")
        # Send to client
        client_socket.sendall(server_message)

client_socket.close()
server_socket.close()