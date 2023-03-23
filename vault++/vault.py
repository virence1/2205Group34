import requests
import random
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

def generatePath():
    nodes=[1,2,3]
    pathToDest = random.sample(nodes,len(nodes))
    sendData(tuple(pathToDest))
    for n in pathToDest:
        print(n)
    
def sendData(order):
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
        function()
    else:
        print(f"Invalid order: {order}")
    

def sendToNode2():
    print("Node 2 Function invoked.")
    pass

def sendToNode3():
    print("Node 3 Function invoked.")
    pass

def sendToNode1():
    print("Node 1 Function invoked.")
    url = "http://20.81.121.55/endpoint1"
    data ={'vote':'Maria', 'nextNode' : 'D', 'remainingPath' : 'D'}
    response = requests.post(url, json=data)

    if response.status_code == 200:
        print(response.text)
        print('Message sent successfully')
    else:
        print('Error sending message: {}'.format(response.text))
    
    return


#sendToNode1()
keyVault()