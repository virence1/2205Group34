import sys
import requests
import random
import json
from azure.identity import UsernamePasswordCredential
from azure.keyvault.secrets import SecretClient
from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient
import hmac
import hashlib
   

def generatePath(vote):
    nodes=[1,2,3]
    pathToDest = random.sample(nodes,len(nodes))
    response=sendData(tuple(pathToDest),vote)

    output_dict = {
    "returnResponse": response
    }
    with open("resultStatus.json", "w") as status_file:
        json.dump(output_dict, status_file)

    return response
    
def sendData(order,vote):
    mapping = {
        (1,2,3) : sendToNode1,
        (1,3,2) : sendToNode1,
        (2,1,3) : sendToNode2,
        (2,3,1) : sendToNode2,
        (3,1,2) : sendToNode3,
        (3,2,1) : sendToNode3
    }
    function = mapping.get(order)
    if function is not None:
        modified_order = ('L',) + order + ('D',)
        response=function(vote, ''.join(map(str, modified_order)))  # use modified_order instead of order
        return response
        
        
    else:
        print(f"Invalid order: {order}")
    
    
def get_secret_string():
    # Define the Azure AD tenant ID, client ID, and client secret
    tenant_id = "7fc78b60-eb18-4991-9d0b-1c06abe3f07e"
    client_id = "08477e2d-4d95-41c2-879f-06e0e1a05956"
    client_secret = "3HU8Q~zh9k7VHZA1NknQtEeeSEt7pumb_6MXwa3N"

# Define the Azure Key Vault URL and secret name
    vault_url = "https://ddd-key-vault.vault.azure.net/"
    secret_name = "tamper-secret"

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
    
def store_secret(name,value):
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

def retrieve_secret(name):
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
def hash_payload(payload):
    # Compute the HMAC-SHA256 digest of the payload using the secret key
    secret_key = get_secret_string()
    payload_str = json.dumps(payload)  # convert the dictionary to a string
    digest = hmac.new(secret_key.encode(), msg=payload_str.encode('utf-8'), digestmod=hashlib.sha256).hexdigest()
    store_secret("PAYLOAD-LIVE-DIGEST", digest)

    # Add the digest to the payload dictionary
    return payload


def verify_digest(payload):
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
            False
        
 
def mapCombo(combo):
    
    if combo == "L123D":
        path = "ZPBGW"
        
    elif combo == "L132D":
        path = "ZPGBW"
        
    elif combo == "L231D":
        path = "ZBGPW"
        
    elif combo == "L213D":
        path = "ZBPGW"    
        
    elif combo == "L312D":
        path = "ZGPBW"
        
    elif combo == "L321D":
        path = "ZGBPW" 
          
    
    return path

def sendToNode2(payload,combo):
    encrypted_path =  mapCombo(combo) # this will map it to what we have agreed upon
    next_node = encrypted_path[1] # updating next node
    remaining_path = encrypted_path[2:]
    payload['combo'] = encrypted_path
    payload['nextNode'] = next_node
    payload['remainingPath'] = remaining_path
    payload['prevNode'] = encrypted_path[0]
    hashed_payload=hash_payload(payload)

    with open('result.json', 'w') as fp:
        json.dump(payload, fp)
    url = "http://20.106.233.101/endpoint2"
    response = requests.post(url, json=hashed_payload)

    if response.status_code == 200:
        return response.text
    else:
        return ('Error sending message: {}'.format(response.text))


def sendToNode3(payload,combo):
    encrypted_path =  mapCombo(combo) # this will map it to what we have agreed upon
    next_node = encrypted_path[1] # updating next node
    remaining_path = encrypted_path[2:]
    payload['combo'] = encrypted_path
    payload['nextNode'] = next_node
    payload['remainingPath'] = remaining_path
    payload['prevNode'] = encrypted_path[0]
    hashed_payload=hash_payload(payload)
    with open('result.json', 'w') as fp:
        json.dump(payload, fp)

    url = "http://20.185.31.43/endpoint3"
    response = requests.post(url, json=hashed_payload)

    if response.status_code == 200:
        return response.text
    else:
        return ('Error sending message: {}'.format(response.text))


def sendToNode1(payload,combo):
    encrypted_path =  mapCombo(combo) # this will map it to what we have agreed upon
    next_node = encrypted_path[1] # updating next node
    remaining_path = encrypted_path[2:]
    payload['combo'] = encrypted_path
    payload['nextNode'] = next_node
    payload['remainingPath'] = remaining_path
    payload['prevNode'] = encrypted_path[0]
    hashed_payload=hash_payload(payload)
    with open('result.json', 'w') as fp:
        json.dump(payload, fp)

    url = "http://20.81.121.55/endpoint1"
    response = requests.post(url, json=hashed_payload)

    if response.status_code == 200:
        return response.text
    else:
        return ('Error sending message: {}'.format(response.text))
    

