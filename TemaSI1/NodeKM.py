import socket
import func

K1 = func.generateRandom16bytes()  # key for ECB/OFB method
K = b'asdeterjsdfwerlg'  # K'
initializedVector = func.generateRandom16bytes()


# Creating socket for communication to A and B
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 8800)
sock.bind(server_address)

# Listening
sock.listen(1)
firstPhaseDone = False

# accepting connection
conn_a, client_address = sock.accept()

# getting encryption method from node A
mode = conn_a.recv(3)
if mode == b'OFB' or mode == b'ECB':
    key = K1
else:
    print('Unknown encryption method')
    exit(1)

encryptedKey = func.encryptBlock(key, mode.decode(), K, func.initVector)
encryptedInitVector = func.encryptBlock(initializedVector, mode.decode(), K, func.initVector)
decryptedKey = func.encryptBlock(encryptedInitVector, mode.decode(), K, func.initVector)

# Send encrypted key and initialized vector to A
conn_a.sendall(encryptedKey)
conn_a.sendall(encryptedInitVector)

# Get the message from A
messageFromA = conn_a.recv(16)

decryptedMessageFromA = func.decryptBlock(messageFromA, mode.decode(), key, initializedVector)
print("\nDecrypted message from A: ", decryptedMessageFromA)

# Bind to node B
sockNodeB = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address_B = ('localhost', 2222)
sockNodeB.connect(server_address_B)

# Send encryption mode and encrypted key to B
sockNodeB.sendall(mode)
sockNodeB.sendall(encryptedKey)
sockNodeB.sendall(encryptedInitVector)

# Get the message from B
encryptedMessageFromB = sockNodeB.recv(16)
decryptedMessageFromB = func.decryptBlock(encryptedMessageFromB, mode.decode(), key, initializedVector)
if decryptedMessageFromA == decryptedMessageFromB:
    conn_a.sendall(b"OK")
    sockNodeB.sendall(b"Ok")
else:
    print("Error decrypting message from A/B")
    exit(2)

blocksFromA = conn_a.recv(16)
print("\nNumber of blocks from node A:", blocksFromA.decode())

blocksFromB = sockNodeB.recv(16)
print("\nNumber of blocks from node B:", blocksFromB.decode())

conn_a.close()
sockNodeB.close()
