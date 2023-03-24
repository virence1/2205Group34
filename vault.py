import sys
import requests
import random
import json
from azure.identity import UsernamePasswordCredential
from azure.keyvault.secrets import SecretClient
from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient

def keyVault():

# Define the Azure AD tenant ID, client ID, and client secret
    tenant_id = "7fc78b60-eb18-4991-9d0b-1c06abe3f07e"
    client_id = "08477e2d-4d95-41c2-879f-06e0e1a05956"
    client_secret = "3HU8Q~zh9k7VHZA1NknQtEeeSEt7pumb_6MXwa3N"

# Define the Azure Key Vault URL and secret name
    vault_url = "https://ddd-key-vault.vault.azure.net/"
    secret_name = "test-secret"

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

    print(secret_value)
    
    
def connect():
    return

def generate():
    return


def store():
    return

def generatePath(vote):
    nodes=[1,2,3]
    pathToDest = random.sample(nodes,len(nodes))
    sendData(tuple(pathToDest),vote)
    for n in pathToDest:
        print(n)
    
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
        function(vote,''.join(map(str,order)))
    else:
        print(f"Invalid order: {order}")
    

def sendToNode2(payload,combo):
    print("Node 2 Function invoked.")
    next_node = combo[1]
    remaining_path = combo[2:]+"D"
    payload['combo'] = f"{combo}D"
    payload['nextNode'] = next_node
    payload['remainingPath'] = remaining_path
    print(payload)

    with open('result.json', 'w') as fp:
        json.dump(payload, fp)
    pass

def sendToNode3(payload,combo):
    print("Node 3 Function invoked.")
    next_node = combo[1]
    remaining_path = combo[2:]+"D"
    payload['combo'] = f"{combo}D"
    payload['nextNode'] = next_node
    payload['remainingPath'] = remaining_path
    print(payload)

    with open('result.json', 'w') as fp:
        json.dump(payload, fp)

    pass

def sendToNode1(payload,combo):
    print("Node 1 Function invoked.")
    next_node = combo[1]
    remaining_path = combo[2:]+"D"
    payload['combo'] = f"{combo}D"
    payload['nextNode'] = next_node
    payload['remainingPath'] = remaining_path
    print(payload)
    
    with open('result.json', 'w') as fp:
        json.dump(payload, fp)

    url = "http://20.81.121.55/endpoint1"
    response = requests.post(url, json=payload)

    if response.status_code == 200:
        print(response.text)
        print('Message sent successfully')
    else:
        print('Error sending message: {}'.format(response.text))
    
    return


#sendToNode1()
#keyVault()
#vote = {"vote": "Maria"}
# vote = {}
# vote['vote'] = "Maria"
#generatePath(vote)