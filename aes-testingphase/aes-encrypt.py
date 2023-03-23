from cryptography.fernet import Fernet
from flask import Flask, request
import requests
import logging
from logging.handlers import RotatingFileHandler
import json
from azure.identity import UsernamePasswordCredential
from azure.keyvault.secrets import SecretClient
from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

app = Flask(__name__)

@app.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"

def sendToNode2(message):
    url = "http://20.106.233.101/endpoint2"
    response = requests.post(url, json=message)
    if response.status_code == 200:
        return "Node 1 received | " + response.text
        print('Message sent successfully')
    else:
        return ('Error sending message: {}'.format(response.text))


def sendToNode3(message):
    url = "http://20.185.31.43/endpoint2"
    response = requests.post(url, json=message)
    if response.status_code == 200:
        return "Node 1 received | " + response.text
        print('Message sent successfully')
    else:
        return('Error sending message: {}'.format(response.text))


def sendToDestination(message):
    url = "http://20.81.124.56/endpointDestination"
    response = requests.post(url, json=message)
    if response.status_code == 200:
        return "Node 1 received | " + response.text
        print('Message sent successfully')
    else:
        return ('Error sending message: {}'.format(response.text))


@app.route("/endpoint1",methods=['POST'])
def receive_message():
    message = request.get_json()
    encrypted_message = aes_encrypt(message)
    if encrypted_message['nextNode'] == '2':
        pathLeft = message['remainingPath']
        newpathLeft = pathLeft[1:]
        response = sendToNode2(message)
        return response

    elif encrypted_message['nextNode'] == '3':
        pathLeft = message['remainingPath']
        newpathLeft = pathLeft[1:]
        response = sendToNode3(message)
        return response

    elif encrypted_message['nextNode'] == 'D':
        message['remainingPath'] = "NULL"
        response = sendToDestination(message)
        return response


def aes_encrypt(payload):
    """
    Encrypt payload using AES encryption with a key retrieved from Azure Key Vault
    :param payload: dict
    :return: dict
    """
    # Define the Azure AD tenant ID, client ID, and client secret
    tenant_id = "7fc78b60-eb18-4991-9d0b-1c06abe3f07e"
    client_id = "08477e2d-4d95-41c2-879f-06e0e1a05956"
    client_secret = "3HU8Q~zh9k7VHZA1NknQtEeeSEt7pumb_6MXwa3N"

    # Define the Azure Key Vault URL and secret name
    vault_url = "https://ddd-key-vault.vault.azure.net/"
    secret_name = "gg.com"

    # Create the credential object
    credential = ClientSecretCredential(
        tenant_id=tenant_id,
        client_id=client_id,
        client_secret=client_secret
    )

    # Create the secret client object and retrieve the secret value
    client = SecretClient(vault_url=vault_url, credential=credential)
    key_bytes = client.get_secret(secret_name).value

    # Encrypt the payload using AES encryption
    key = key_bytes[:32]  # Use only the first 32 bytes of the key
    iv = Fernet.generate_key()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(json.dumps(payload).encode()) + encryptor.finalize()
    encrypted_payload = {
        "ciphertext": ciphertext.hex(),
        "iv": iv.hex(),
    }

    return encrypted_payload