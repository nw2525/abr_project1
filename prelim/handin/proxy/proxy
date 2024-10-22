#!/usr/bin/env python3.10

from socket import *
import sys

# Variables from command line
listen_port = sys.argv[1]   # receive from client
fake_ip = sys.argv[2]       # 127.0.0.1
server_ip = sys.argv[3]     # 127.0.0.1
server_port = '8080'   # send to server

# Set up proxy
proxySocket = socket(AF_INET, SOCK_STREAM)
proxySocket.bind((str(fake_ip), int(listen_port)))
proxySocket.listen(1)

eom = '\n'
buffer = ''

while True:
    try:
        clientSocket, addr = proxySocket.accept()
        proxySocket = socket(AF_INET, SOCK_STREAM)
        proxySocket.connect((str(server_ip), int(server_port)))
        
        while True:
            clientMessage = clientSocket.recv(2048)
            print('Revceived Message from Client:', clientMessage.decode())
            if clientMessage == 0:
                print('Client disconnected.')
                break
            else:
                # Buffer message until EOM is detected
                # Send buffer up until the EOM to server
                # Reset buffer and loads it up with the rest of the message
                eomPos = clientMessage.decode().find(eom)
                if eomPos != -1:
                    buffer += clientMessage.decode()[0:eomPos+len(eom)]
                    print('Sending message to server:', buffer)
                    proxySocket.send(buffer.encode())
                    buffer = clientMessage.decode()[eomPos+len(eom):]
                    serverMessage = proxySocket.recv(2048)
                    print('Server message:', serverMessage.decode())
                    if serverMessage == 0:
                        print('Server disconnected.')
                        break
                    clientSocket.send(serverMessage)
                else: 
                    buffer += clientMessage.decode()
                print('Sending message to server:', buffer)
                proxySocket.send(buffer.encode())
                buffer = ''
                serverMessage = proxySocket.recv(2048)
                print('Server message:', serverMessage.decode())
    except:
        break

clientSocket.close()
proxySocket.close()