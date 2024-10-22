from socket import *

serverSocket = socket(AF_INET, SOCK_DGRAM)

serverSocket.bind(('' , 8080))

# Recieving message from client
clientMessage, clientAddress = serverSocket.recvfrom(2048)


print("Received Message from Client: ", clientMessage.decode())

# Modifying the message
clientMessage = clientMessage.decode().upper()

print("Sending Message to Client: ", clientMessage)

# Sending the encoded modified message back to the client
serverSocket.sendto(clientMessage.encode(), clientAddress)

serverSocket.close()