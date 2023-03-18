from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util import Padding
import requests
import base64
import binascii

def encrypt_string(message, key):
    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(key, AES.MODE_GCM, iv)
    padded_message = Padding.pad(message.encode('utf-8'), AES.block_size)
    ciphertext, tag = cipher.encrypt_and_digest(padded_message)
    return iv, ciphertext, tag


def decrypt_string(iv, ciphertext, tag, key):
    cipher = AES.new(key, AES.MODE_GCM, iv)
    padded_message = cipher.decrypt_and_verify(ciphertext, tag)
    message = Padding.unpad(padded_message, AES.block_size)
    return message.decode('utf-8')


def DH_AES():
    message = "This is a secret message"
    key = get_random_bytes(32)
    iv, ciphertext, tag = encrypt_string(message, key)
    decrypted_message = decrypt_string(iv, ciphertext, tag, key)

    print("Original message: ", message)
    print("Key: ", key.hex())
    print("IV: ", iv.hex())
    print('Ciphertext: ', binascii.hexlify(ciphertext).decode('utf-8'))
    print('Tag: ', binascii.hexlify(tag).decode('utf-8'))
    print("Decrypted message: ", decrypted_message)
    print("\n")
    return iv + ciphertext + tag


def sendToServer(payload):
    
    url = "http://20.185.31.43/endpoint3"
    
    data = {'message': base64.b64encode(payload).decode('utf-8')}
    response = requests.post(url, json=data)

    if response.status_code == 200:
        print('Message sent successfully >>> ' + str(data))
        print('Message server reply >>> ' + response.text)
        ciphertext = payload[AES.block_size:-AES.block_size]
        ciphertext_hex = binascii.hexlify(ciphertext).decode('utf-8')
        print('Ciphertext:', ciphertext_hex)
    else:
        print('Error sending message: {}'.format(response.text))

    return

payload = DH_AES()
sendToServer(payload)
