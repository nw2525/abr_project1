# for testing purposes
from socket import *
import sys

clientSocket = socket(AF_INET, SOCK_STREAM)

serverName = 'localhost'
serverPort = int(sys.argv[1])

# Connect to the server's listening socket
clientSocket.connect((serverName, serverPort))

while True:
    message = input("Input your message: ")
    print("Sending Message to Server: ", message)

    # Send the encoded message to the server
    clientSocket.send(message.encode())

    if message == 'exit':
        serverMessage = clientSocket.recv(2048)
        print("Received Message from Server: ", serverMessage.decode())
        clientSocket.close()
        break