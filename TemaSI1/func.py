from Crypto import Random
from Crypto.Cipher import AES


blockSize = 16
initVector = b'aabbccddeeffgghh'


def generateRandom16bytes():
    return Random.get_random_bytes(16)


def encryptBlock(block, mode, key, iv):
    encryptedBlock = 0
    if mode == "OFB":
        modeType = AES.MODE_OFB
        aesObj = AES.new(key, modeType, iv)
        encryptedIv = aesObj.encrypt(iv)
        encryptedBlock = xor(encryptedIv, block)
    elif mode == "ECB":
        modeType = AES.MODE_ECB
        aesObj = AES.new(key, modeType)
        encryptedBlock = aesObj.encrypt(block)

    return encryptedBlock


def decryptBlock(block, mode, key, iv):
    if mode == "OFB":
        modeType = AES.MODE_OFB
        aesObj = AES.new(key, modeType, iv)
        cypherEncryption = aesObj.encrypt(iv)
        Text = xor(cypherEncryption, block)
    elif mode == "ECB":
        modeType = AES.MODE_ECB
        aesObj = AES.new(key, modeType)
        decryptedBlock = aesObj.decrypt(block)
        Text = decryptedBlock

    return Text


def xor(ba1, ba2):
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])
