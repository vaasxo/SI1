import socket
import func
from Crypto.Util.Padding import pad

K = b'asdeterjsdfwerlg'

# creating a socket for the KM node and connecting to it
sockNodeKM = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address_KM = ('localhost', 8800)
sockNodeKM.connect(server_address_KM)

# Choose the encryption mode and send it to KM
print("Choose OFB or ECB: ")
mode = input().upper()

binMode = str.encode(mode)
sockNodeKM.sendall(binMode)

# Receiving and decrypting the key and vector from KM
encryptedKey = sockNodeKM.recv(16)
initializedVector = sockNodeKM.recv(16)

decryptedKey = func.decryptBlock(encryptedKey, mode, K, func.initVector)
decryptedVector = func.decryptBlock(initializedVector, mode, K, func.initVector)

print("\nDecrypted key is:", decryptedKey)
print("\nDecrypted vector is:", decryptedVector)

# encrypt block with new decrypted key and send it back to KM
encryptedBlock = func.encryptBlock(b"Between A and B ", mode, decryptedKey, decryptedVector)
sockNodeKM.sendall(encryptedBlock)

# receive message from KM in order to continue communication
messageForCommunication = sockNodeKM.recv(2)
print("\nMessage received from KM regarding the communication A-B: ", messageForCommunication.decode())
sockNodeB = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where node B is listening
server_address_B = ('localhost', 2222)
if messageForCommunication == b"OK":
    f = open("input", "r")
    input_text = f.read()
    nrOfBlocks = len(input_text) / func.blockSize
    if nrOfBlocks > int(nrOfBlocks):
        nrOfBlocks = nrOfBlocks + 1
    sockNodeB.connect(server_address_B)

    # Sending number of blocks to KM node
    sockNodeB.sendall(str(int(nrOfBlocks)).encode())
    sockNodeKM.sendall(str(int(nrOfBlocks)).encode())
    i = 0
    pos = 0
    while i < int(nrOfBlocks):
        block = input_text[pos: pos + func.blockSize]
        pos = pos + func.blockSize
        if int(nrOfBlocks) - i == 1:
            block = pad(block.encode(), 16).decode()
        print("Block is:", block)
        encryptedInput = func.encryptBlock(block.encode(), mode, decryptedKey, decryptedVector)
        sockNodeB.sendall(encryptedInput)
        decryptedVector = encryptedInput
        i = i + 1

    sockNodeB.close()
    sockNodeKM.close()
