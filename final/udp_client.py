from socket import *

clientSocket = socket(AF_INET, SOCK_DGRAM)

serverName = 'localhost'
serverPort = 8080

message = input("Input your message: ")

print("Sending Message to Server: ", message)

# Send message to the server using the server's address
clientSocket.sendto(message.encode(), (serverName, serverPort))

# Receive the modified message back from the server
serverMessage, serverAddress = clientSocket.recvfrom(2048)

print("Received Message from Server: ", serverMessage.decode())

clientSocket.close()