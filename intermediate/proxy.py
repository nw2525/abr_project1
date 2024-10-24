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

file = open(log, "w")
# Set up proxy
proxy_socket = socket(AF_INET, SOCK_STREAM)
proxy_socket.bind((str(fake_ip), int(listen_port)))
# proxy_socket.listen(1)

while True:
    # connect to client(s)
    proxy_socket.listen(1)
    client_socket, addr = proxy_socket.accept()

    # connect to server
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.connect((str(server_ip), int(server_port)))
    connected = True
    start = time.time()

    while connected:
        ### maybe check if still connected to client(s)/server
        print("Waiting on message from client...")
        client_request = client_socket.recv(65536)
        print("Request received from client")
        server_socket.send(client_request)
        print("Request sent to server")
        chunk_start = time.time()

        buffer = b""
        header_end = b"\r\n\r\n" 
        print("Receiving header...")
        while header_end not in buffer:
            buffer += server_socket.recv(65536)

        print("Header received. Processing...")
        header, _, body = buffer.partition(header_end)
        header_str = header.decode()
        header_length = len(header)

        # Arbitrary chunk name to check for errors easily
        chunk_name = "foobar"
        for line in header_str.splitlines():
            if line.lower().startswith("content-length"):
                content_length = int(line.split(":")[1].strip())
                chunk_size = header_length + content_length

        print("Header processed. Buffering chunks...")
        while len(buffer) < chunk_size:
            chunk = server_socket.recv(65536)
            if not chunk:
                break
            buffer += chunk

        print("Full chunk received from server")
        end = time.time()
        duration = end - chunk_start
        output = str(end) + " " + str(duration) + " " + server_ip + " " + chunk_name + " " + str(chunk_size)
        print(output)
        file.write(output + "\n")

        print("Sending chunk to client...")
        client_socket.sendall(buffer)
        print("Chunk sent to client")

    client_socket.close()
    server_socket.close()