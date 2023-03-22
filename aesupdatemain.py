import base64
import binascii
import requests
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util import Padding
from secretvault import keyVault

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
    return iv, ciphertext, tag, key


def sendToServer(iv, ciphertext, tag, key):
    url = "http://20.81.124.56/endpointDestination"
    # url = "http://20.185.31.43/endpoint3" 
    data = {'iv': binascii.hexlify(iv).decode('utf-8'),
            'ciphertext': base64.b64encode(ciphertext).decode('utf-8'),
            'tag': binascii.hexlify(tag).decode('utf-8'),
            'key': binascii.hexlify(key).decode('utf-8')}
    response = requests.post(url, json=data)

    if response.status_code == 200:
        print('Message sent successfully >>> ' + str(data))
        print('Message server reply >>> ' + response.text)
        with open('sendToServer_history.txt', 'a') as f:
            f.write('IV: ' + binascii.hexlify(iv).decode('utf-8') + '\n')
            f.write('Ciphertext: ' + binascii.hexlify(ciphertext).decode('utf-8') + '\n')
            f.write('Tag: ' + binascii.hexlify(tag).decode('utf-8') + '\n')
            f.write('Key: ' + binascii.hexlify(key).decode('utf-8') + '\n')
            f.write('Server Reply: ' + response.text + '\n\n')
    else:
        print('Error sending message: {}'.format(response.text))

    return

iv, ciphertext, tag, key = DH_AES()
# Store the IV, key, and tag in the Key Vault
keyVault('set', 'iv', iv.hex())
keyVault('set', 'key', key.hex())
keyVault('set', 'tag', tag.hex())

print("Stored IV: ", keyVault('get', 'iv'))
print("Stored Key: ", keyVault('get', 'key'))
print("Stored Tag: ", keyVault('get', 'tag'))

sendToServer(iv, ciphertext, tag, key)