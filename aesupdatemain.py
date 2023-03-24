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




def sendToNode1(message):
    url = "http://20.81.121.55/endpoint1"
    response = requests.post(url, json=message)
    if response.status_code == 200:
        return "Node 1 received | " + response.text
        print('Message sent successfully')
    else:
        return ('Error sending message: {}'.format(response.text))

def sendToNode3(message):
    url = "http://20.185.31.43/endpoint3"
    response = requests.post(url, json=message)
    if response.status_code == 200:
        return "Node 3 received | " + response.text
        print('Message sent successfully')
    else:
        return('Error sending message: {}'.format(response.text))

def sendToDestination(message):
    url = "http://20.81.124.56/endpointDestination"
    response = requests.post(url, json=message)
    if response.status_code == 200:
        return "Destination received | " + response.text
        print('Message sent successfully')
    else:
        return ('Error sending message: {}'.format(response.text))

def receive_message():
    message = request.get_json()
    encrypted_message = aes_encrypt(message)
    if encrypted_message['nextNode'] == '3':
        pathLeft = message['remainingPath']
        newpathLeft = pathLeft[1:]
        response = sendToNode3(message)
        return response
    elif encrypted_message['nextNode'] == '1':
        pathLeft = message['remainingPath']
        newpathLeft = pathLeft[1:]
        response = sendToNode1(message)
        return response
    elif encrypted_message['nextNode'] == 'D':
        message['remainingPath'] = "NULL"
        response = sendToDestination(message)
        return response

def aes_encrypt(payload):
    # Define the Azure AD tenant ID, client ID, and client secret
    tenant_id = "7fc78b60-eb18-4991-9d0b-1c06abe3f07e"
    client_id = "08477e2d-4d95-41c2-879f-06e0e1a05956"
    client_secret = "3HU8Q~zh9k7VHZA1NknQtEeeSEt7pumb_6MXwa3N"

    # Define the Azure Key Vault URL
    vault_url = "https://ddd-key-vault.vault.azure.net/"

    # Create the credential object
    credential = ClientSecretCredential(
        tenant_id=tenant_id,
        client_id=client_id,
        client_secret=client_secret
    )

    # Create the secret client object
    client = SecretClient(vault_url=vault_url, credential=credential)

    # Generate a random AES key and IV
    key = get_random_bytes(32)
    iv = get_random_bytes(AES.block_size)

    # Encrypt the message using AES-GCM
    cipher = AES.new(key, AES.MODE_GCM, iv)
    padded_message = Padding.pad(payload['vote'].encode('utf-8'), AES.block_size)
    ciphertext, tag = cipher.encrypt_and_digest(padded_message)



    secretkey=payload['user'] + "-AES-KEY"
    secretiv=payload['user'] + "-AES-IV"
    secrettag=payload['user'] + "-AES-TAG"
    
    client.set_secret(name=secretkey, value=binascii.hexlify(key).decode('utf-8'))
    client.set_secret(name=secretiv, value=binascii.hexlify(iv).decode('utf-8'))
    client.set_secret(name=secrettag, value=binascii.hexlify(tag).decode('utf-8'))
        
    # Update the payload with the encrypted message
   # vote = binascii.hexlify(ciphertext).decode('utf-8')
    #vote = base64.b64encode(ciphertext + tag).decode('utf-8')
    vote = base64.b64encode(ciphertext).decode('utf-8')
    payload['vote'] = vote

    return payload
#json_payload = {'vote': 'gg', 'combo':'132D', 'nextNode': 'None', 'remainingPath':'None', 'user': 'account_username'}
json_payload = {"vote": "aacbc", "user": "X2398754Y", "combo": "231D", "nextNode": "3", "remainingPath": "1D"}
aes_encrypt(json_payload)
print(json_payload)