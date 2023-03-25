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
    if response.status_code == 200: # node 2 got it successfully
        return "20" + response.text
    else:
        return  "70"



def sendToNode3(message):
    url = "http://20.185.31.43/endpoint3"
    response = requests.post(url, json=message)
    if response.status_code == 200:
        return "30" + response.text
    else:
        return "80"




def sendToDestination(message):
    url = "http://20.81.124.56/endpointDestination"
    response = requests.post(url, json=message)
    if response.status_code == 200:
        return "40" + response.text
    else:
        return  "90"
        
        
def get_secret_string(): # NOTHING TO CHANGE HERE 
    # Define the Azure AD tenant ID, client ID, and client secret
    tenant_id = "7fc78b60-eb18-4991-9d0b-1c06abe3f07e"
    client_id = "08477e2d-4d95-41c2-879f-06e0e1a05956"
    client_secret = "3HU8Q~zh9k7VHZA1NknQtEeeSEt7pumb_6MXwa3N"

# Define the Azure Key Vault URL and secret name
    vault_url = "https://ddd-key-vault.vault.azure.net/"
    secret_name = "tamper-secret" #default pre fixed random key that I generated that is stored in the vault

# Define the username and password for the user you want to authenticate as

# Create the credential object
    credential = ClientSecretCredential(
    tenant_id=tenant_id,
    client_id=client_id,
    client_secret=client_secret
    )

# Create the secret client object and retrieve the secret value
    client = SecretClient(vault_url=vault_url, credential=credential)
    secret_value = client.get_secret(secret_name).value
    
    return secret_value

def store_secret(name,value): # NOTHING TO CHANGE HERE
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

    # Create the secret client object and store the secret value
    client = SecretClient(vault_url=vault_url, credential=credential)
    client.set_secret(name, value)
    
    return

def retrieve_secret(name): # NOTHING TO CHANGE HERE
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

    # Create the secret client object and store the secret value
    client = SecretClient(vault_url=vault_url, credential=credential)
    secret_value = client.get_secret(name).value
    return secret_value
    

def hash_payload(payload): # NEED TO CHANGE FOR UR OWN NODE 
    # Compute the HMAC-SHA256 digest of the payload using the secret key
    secret_key = get_secret_string()
    payload_str = json.dumps(payload)  # convert the dictionary to a string
    digest = hmac.new(secret_key.encode(), msg=payload_str.encode('utf-8'), digestmod=hashlib.sha256).hexdigest()
    store_secret("PAYLOAD-NODE1-DIGEST", digest) # CHANGE THIS TO REFLECT UR OWN NODE NUMBER
    return payload


def verify_digest(payload): # THERE WILL NOT BE A FUNCTION FOR DESTINATION AS DESTINATION IS THE LAST THING IN THE PATH
    if payload['prevNode'] == 'Z': # THIS MEANS THAT PAYLOAD CAME FROM LIVE SERVER
        secret_key =  get_secret_string()
        prev_node_digest = retrieve_secret("PAYLOAD-LIVE-DIGEST")
        payload_str = json.dumps(payload)
        computed_digest = hmac.new(secret_key.encode(), msg=payload_str.encode('utf-8'), digestmod=hashlib.sha256).hexdigest()
        if computed_digest == prev_node_digest:
            return True
        else:
            return False
    elif payload['prevNode'] == 'P': # THIS MEANS THAT PAYLOAD CAME FROM NODE 1
        secret_key =  get_secret_string()
        prev_node_digest = retrieve_secret("PAYLOAD-NODE1-DIGEST")
        payload_str = json.dumps(payload)
        computed_digest = hmac.new(secret_key.encode(), msg=payload_str.encode('utf-8'), digestmod=hashlib.sha256).hexdigest()
        if computed_digest == prev_node_digest:
            return True
        else:
            return False
    elif payload['prevNode'] == 'B': # THIS MEANS THAT PAYLOAD CAME FROM NODE 2
        secret_key =  get_secret_string()
        prev_node_digest = retrieve_secret("PAYLOAD-NODE2-DIGEST")
        payload_str = json.dumps(payload)
        computed_digest = hmac.new(secret_key.encode(), msg=payload_str.encode('utf-8'), digestmod=hashlib.sha256).hexdigest()
        if computed_digest == prev_node_digest:
            return True
        else:
            return False
    elif payload['prevNode'] == 'G': # THIS MEANS THAT PAYLOAD CAME FROM NODE 3
        secret_key =  get_secret_string()
        prev_node_digest = retrieve_secret("PAYLOAD-NODE3-DIGEST")
        payload_str = json.dumps(payload)
        computed_digest = hmac.new(secret_key.encode(), msg=payload_str.encode('utf-8'), digestmod=hashlib.sha256).hexdigest()
        if computed_digest == prev_node_digest:
            return True
        else:
            return False
            
@app.route("/endpoint1",methods=['POST'])
def receive_message():
    message=request.get_json()
    result=verify_digest(message)
    if result == True:
        encrypted_message = rsa_encrypt(message) # CHANGE THIS TO UR OWN ALGO ENCRYPT FUNCTION
        nextNode = encrypted_message['remainingPath'][0]
        if nextNode == 'B':
            updatedPathLeft = encrypted_message['remainingPath'][1:]
            encrypted_message['remainingPath'] = updatedPathLeft
            encrypted_message['prevNode'] = 'P' # CHANGE THIS TO UR OWN NODE NUMBER'S LETTER
            hashed_payload=hash_payload(payload)
            response = sendToNode2(hashed_payload)
            return "10UWU"+response #update the number before UWU to ur own node
        elif nextNode == 'G':
            updatedPathLeft = encrypted_message['remainingPath'][1:]
            encrypted_message['remainingPath'] = updatedPathLeft
            encrypted_message['prevNode'] = 'P' # CHANGE THIS TO YOUR OWN NODE NUMBER'S LETTER
            hashed_payload=hash_payload(payload)
            response = sendToNode3(hashed_payload)
            return "10UWU"+response #update the number before UWU to ur own node
        elif nextNode == 'W':
            updatedPathLeft = encrypted_message['remainingPath'][1:]
            encrypted_message['remainingPath'] = updatedPathLeft
            encrypted_message['prevNode'] = 'P' # CHANGE THIS TO YOUR OWN NODE NUMBER'S LETTER
            hashed_payload=hash_payload(payload)
            response = sendToDestination(hashed_payload)
            return "10UWU"+response #update the number before UWU to ur own node
    else:
        return "NOUWU"



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
    private_key_str = private_key_bytes.decode('utf-8')
    secretname=payload['user']+"-"+"RSA"+"-PRIVATEKEY"
    client.set_secret(name=secretname, value=private_key_str)
    payload['vote'] = encrypted_message.hex()
    return payload

if __name__ == "__main__":
    app.run(host='0.0.0.0')