from flask import Flask , request
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

app = Flask(__name__)

@app.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"

def sendToNode2(message):
    url = "http://20.106.233.101/endpoint2"
    response = requests.post(url, json=message)
    if response.status_code == 200:
        return "Node 1 recieved | " + response.text
        print('Message sent successfully')
    else:
        return ('Error sending message: {}'.format(response.text))



def sendToNode3(message):
    url = "http://20.185.31.43/endpoint2"
    response = requests.post(url, json=message)
    if response.status_code == 200:
        return "Node 1 recieved | " + response.text
        print('Message sent successfully')
    else:
        return('Error sending message: {}'.format(response.text))




def sendToDestination(message):
    url = "http://20.81.124.56/endpointDestination"
    response = requests.post(url, json=message)
    if response.status_code == 200:
        return "Node 1 recieved | " + response.text
        print('Message sent successfully')
    else:
        return ('Error sending message: {}'.format(response.text))
        
        
@app.route("/endpoint1",methods=['POST'])
def receive_message():
    message=request.get_json()
    encrypted_message=rsa_encrypt(message)
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

    elif encrypted_ message['nextNode'] == 'D':
        message['remainingPath'] = "NULL"
        response = sendToDestination(message)
        return response



def rsa_encrypt(payload):
# Define the Azure AD tenant ID, client ID, and client secret
    tenant_id = "7fc78b60-eb18-4991-9d0b-1c06abe3f07e"
    client_id = "08477e2d-4d95-41c2-879f-06e0e1a05956"
    client_secret = "3HU8Q~zh9k7VHZA1NknQtEeeSEt7pumb_6MXwa3N"

# Define the Azure Key Vault URL and secret name
    vault_url = "https://ddd-key-vault.vault.azure.net/"
    
# Create the credential object
    credential = ClientSecretCredential(
    tenant_id=tenant_id,
    client_id=client_id,
    client_secret=client_secret
    )

# Create the secret client object and retrieve the secret value
    client = SecretClient(vault_url=vault_url, credential=credential)

# Generating an RSA Key Pair
    private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)
    public_key = private_key.public_key()
    
    vote = payload['vote'].encode('utf-8')
    encrypted_message = public_key.encrypt(
    vote,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)
    private_key_bytes = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)
    client.set_secret(name='shammie-uwu-rsa-private-key', value=private_key_bytes)
    payload['vote'] = encrypted_message.hex()
    return payload

if __name__ == "__main__":
    app.run(host='0.0.0.0')
