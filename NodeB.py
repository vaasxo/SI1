import socket

import func

K = b'gertfndsfpoiewjt'

# Create the socket for node B
sockNodeB = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address_B = ('localhost', 2222)
sockNodeB.bind(server_address_B)

sockNodeB.listen(1)
conn_b, client = sockNodeB.accept()

# read from KM
mode = conn_b.recv(3)
encryptedKey = conn_b.recv(16)
encryptedIV = conn_b.recv(16)
print(encryptedKey, mode, K)

decryptedKey = func.decryptBlock(encryptedKey, mode.decode(), K, func.initVector)
decryptedIV = func.decryptBlock(encryptedIV, mode.decode(), K, func.initVector)

print("\nDecrypted key:", decryptedKey)
print("\nDecrypted vector:", decryptedIV)

encryptedMessage = func.encryptBlock(b"Between A and B ", mode.decode(), decryptedKey, decryptedIV)
conn_b.sendall(encryptedMessage)
successMessageFromKM = conn_b.recv(2)
print("\nStatus from KM:", successMessageFromKM.decode())

# Accepting the node A
conn_a, client_a = sockNodeB.accept()
print('\nConnected to A')

nrInBytes = conn_a.recv(2)
print(nrInBytes.decode('utf-8'))
numberOfBlocks = int(float(nrInBytes.decode('utf-8')))
conn_b.sendall(str(numberOfBlocks).encode())
finalMessage = ''

while numberOfBlocks > 0:
    block = conn_a.recv(16)
    decryptedMessage = func.decryptBlock(block, mode.decode(), decryptedKey, decryptedIV)
    decryptedIV = block
    numberOfBlocks = numberOfBlocks - 1
    finalMessage = finalMessage + decryptedMessage.decode('utf-8')

print("\nMessage from A: ", finalMessage)
conn_a.close()
sockNodeB.close()
