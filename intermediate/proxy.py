from socket import *
import requests
import sys
import threading
import time

assert len(sys.argv) == 3, "Error: Expected 4 arguments. Usage: ./proxy <log> <listen-port> <fake-ip> <server-ip>"

# Variables from command line
log = sys.argv[1]
listen_port = sys.argv[2]   # receive from client
fake_ip = sys.argv[3]       # 127.0.0.1
server_ip = sys.argv[4]     # 127.0.0.1
server_port = '8080'   # send to server

file = open(log, "a")
# Set up proxy
proxy_socket = socket(AF_INET, SOCK_STREAM)
proxy_socket.bind((str(fake_ip), int(listen_port)))
proxy_socket.listen(1)

while True:
    try:
        # don't forget threading
        # connect to client(s)
        client_socket, addr = proxy_socket.accept()

        # connect to server
        proxy_socket = socket(AF_INET, SOCK_STREAM)
        proxy_socket.connect((str(server_ip), int(server_port)))
        connected = True
        start = time.time()
        while connected:
            ### maybe check if still connected to client(s)/server
            # I don't think client is sending anything to server?
            # clientMessage = client_socket.recv(2048)
            # proxy_socket.send(clientMessage.encode())

            chunk_start = time.time()
            server_message = proxy_socket.recv(2048)
            end = time.time()

            # No response from server
            if server_message == 0:
                break
            
            # Process chunk for log
            duration = end - chunk_start
            header = chunk_start.decode().split("\n")[0]
            chunk_name = header.split(" ")[1]
            chunk_size = len(server_message)

            output = str(end) + " " + str(duration) + " " + server_ip + " " + chunk_name + " " + chunk_size
            file.write(output + "\n")
            # print(output)
            file.flush()
            
            # Send to client
            proxy_socket.send(server_message)
    except:
        break

client_socket.close()
proxy_socket.close()