from flask import Flask, request
import requests
import logging
from logging.handlers import RotatingFileHandler
import json
from azure.identity import UsernamePasswordCredential
from azure.keyvault.secrets import SecretClient
from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
import base64
import binascii
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util import Padding
from secretvault import keyVault


##
def aes_encrypt(payload):
    message = "A"
    key = get_random_bytes(32)

    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(key, AES.MODE_GCM, iv)
    padded_message = Padding.pad(message.encode('utf-8'), AES.block_size)
    ciphertext, tag = cipher.encrypt_and_digest(padded_message)

    # Store the IV, key, and tag in the Key Vault
    keyVault('set', 'X2398754Y-AES-IV', iv.hex())
    keyVault('set', 'X2398754Y-AES-KEY', key.hex())
    keyVault('set', 'X2398754Y-AES-TAG', tag.hex())

    # Print the IV, key, and tag
    print("IV: " + iv.hex())
    print("Key: " + key.hex())
    print("Tag: " + tag.hex())

    payload['vote'] = base64.b64encode(ciphertext).decode('utf-8')

    url = "http://20.81.124.56/endpointDestination"
    response = requests.post(url, json=payload)

    if response.status_code == 200:
        print('Message sent successfully >>> ' + str(payload))
        print('Message server reply >>> ' + response.text)
        with open('sendToServer_history.txt', 'a') as f:
            f.write('IV: ' + binascii.hexlify(iv).decode('utf-8') + '\n')
            f.write('vote: ' + binascii.hexlify(ciphertext).decode('utf-8') + '\n')
            f.write('Tag: ' + binascii.hexlify(tag).decode('utf-8') + '\n')
            f.write('Key: ' + binascii.hexlify(key).decode('utf-8') + '\n')
            f.write('Server Reply: ' + response.text + '\n\n')
    else:
        print('Error sending message: {}'.format(response.text))

payload = {}
aes_encrypt(payload)

