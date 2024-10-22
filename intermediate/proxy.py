from socket import *
import requests
import sys
import time

assert len(sys.argv) == 3, "Error: Expected 4 arguments. Usage: ./proxy <log> <listen-port> <fake-ip> <server-ip>"

# Variables from command line
log = sys.argv[1]
listen_port = sys.argv[2]   # receive from client
fake_ip = sys.argv[3]       # 127.0.0.1
server_ip = sys.argv[4]     # 127.0.0.1
server_port = '8080'   # send to server

file = open(log, "w")
# Set up proxy
proxySocket = socket(AF_INET, SOCK_STREAM)
proxySocket.bind((str(fake_ip), int(listen_port)))
proxySocket.listen(1)

while True:
    try:
        # don't forget threading
        # connect to client(s)
        clientSocket, addr = proxySocket.accept()
        proxySocket = socket(AF_INET, SOCK_STREAM)
        proxySocket.connect((str(server_ip), int(server_port)))
        connected = True
        start = time.time()
        while connected:
            ### maybe check if still connected to client(s)/server

            # receive message from client(s)
            # connect to server
            # send chunk request to server
            chunk_start = time.time()
            # get chunk from server
            end = time.time()
            duration = end - chunk_start
            # process chunk
            chunk_name = "foobar"
            output = str(end) + " " + str(duration) + " " + server_ip + " " + chunk_name
            print(output)
            file.write(output + "\n")
            # send chunk to client
    except:
        break