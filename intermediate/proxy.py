#!/usr/bin/env python3.10

import os
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
server_port = '80'          # send to server

def handle_client(client_socket, log, server_ip, server_port):
    if os.path.exists(log):
        os.remove(log)

    # Connect to server
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.connect((str(server_ip), int(server_port)))
    connected = True
    start = time.time()

    header_end = b"\r\n\r\n"
    buffer = b""
    while connected:
        file = open(log, "a")
        client_request = 0
        while not client_request:
            client_request = client_socket.recv(8192)
        # print("Request received from client: ", len(client_request))

        header, _, body = client_request.partition(header_end)
        header_str = header.decode()
        request_line = header_str
        chunk_name = request_line.split(" ")[1]

        server_socket.send(client_request)
        # print("Request sent to server")
        chunk_start = time.time()

        # print("Receiving header...")
        while header_end not in buffer:
            server_message = server_socket.recv(8192)
            buffer += server_message

        # print("Header received. Processing...")
        header, _, body = buffer.partition(header_end)
        header_str = header.decode()
        header_length = len(header) + len(header_end)

        # Find content length
        for line in header_str.splitlines():
            if line.lower().startswith("content-length"):
                content_length = int(line.split(":")[1].strip())
                chunk_size = header_length + content_length
                break
        # print("Receiving server message...")
        while len(buffer) < chunk_size:
            server_message = server_socket.recv(8192)
            if not server_message:
                break
            buffer += server_message
        
        cutoff = len(buffer) - chunk_size 
        # print("Sending chunk to client...")
        if cutoff == 0:
            client_socket.sendall(buffer)
            buffer = b""
        else:
            client_socket.sendall(buffer[:-cutoff])
            buffer = buffer[-cutoff:]
        # print("Chunk sent to client")

        end = time.time()
        duration = end - chunk_start

        output = str(end) + " " + str(duration) + " " + server_ip + " " + chunk_name + " " + str(chunk_size)
        print(output)
        sys.stdout.flush()
        file.write(output + "\n")
        file.close()

    client_socket.close()
    server_socket.close()

proxy_socket = socket(AF_INET, SOCK_STREAM)
proxy_socket.bind((str(fake_ip), int(listen_port)))
proxy_socket.listen(1)
client_socket, addr = proxy_socket.accept()

while True:
    client_socket, addr = proxy_socket.accept()
    client_thread = threading.Thread(target=handle_client, args=(client_socket, log, server_ip, server_port))
    client_thread.start()