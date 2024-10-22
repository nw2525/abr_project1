# for testing purposes
from socket import *
import sys
import time

serverSocket = socket(AF_INET, SOCK_STREAM)

serverPort = int(sys.argv[1])
serverSocket.bind(('' , serverPort))

serverSocket.listen(1)

connectionSocket, addr = serverSocket.accept()

while True:
    try:
        # Recieving message from client
        clientMessage = connectionSocket.recv(2048)
        
        if clientMessage.decode() == '':
            continue

        print("Received Message from Client: ", clientMessage.decode())

        # Modifying the message
        clientMessage = clientMessage.decode().upper()

        print("Sending Message to Client: ", clientMessage)

        # Sending the encoded modified message back to the client
        connectionSocket.send(clientMessage.encode())
    except KeyboardInterrupt:
        print("Keyboard Interrupt")
        pass


connectionSocket.close()
serverSocket.close()