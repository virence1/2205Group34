import sys
import json
import base64
import requests
import random
from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient


# Retrieve the filename of the JSON payload from the command-line argument
filename = sys.argv[1]
#filename = "temp_payload.json"

# Load the JSON payload from the file
with open(filename, 'r') as f:
    json_payload = json.load(f)

# Extract the encrypted vote, key, and IV from the JSON payload
print("JSON variables in temp file:")
print(json_payload['vote'])
print(json_payload['key'])
print(json_payload['iv'])
print('\n')

#Decoding bytes
encrypted_vote = base64.b64decode(json_payload['vote'])
key = base64.b64decode(json_payload['key'])
iv = base64.b64decode(json_payload['iv'])


# For debugging purposes, print the readable form (orignal is a byte string)
#encrypted_vote_string = encrypted_vote.decode('utf-8')
#key_string = key.decode('utf-8')
#iv_string = iv.decode('utf-8')

#print(encrypted_vote)
#print(key)
#print(iv)

def keyVault(mode, secret_name, secret_value_to_store=None):
    tenant_id = "7fc78b60-eb18-4991-9d0b-1c06abe3f07e"
    client_id = "08477e2d-4d95-41c2-879f-06e0e1a05956"
    client_secret = "3HU8Q~zh9k7VHZA1NknQtEeeSEt7pumb_6MXwa3N"

    vault_url = "https://ddd-key-vault.vault.azure.net/"

    credential = ClientSecretCredential(
        tenant_id=tenant_id,
        client_id=client_id,
        client_secret=client_secret
    )
    client = SecretClient(vault_url=vault_url, credential=credential)

    if mode == 'set':
        client.set_secret(secret_name, secret_value_to_store)
        return f"Secret {secret_name} stored successfully."
    elif mode == 'get':
        secret_value = client.get_secret(secret_name).value
        return secret_value
    else:
        return "Invalid mode. Use 'set' or 'get'."
    
secret_key = json_payload['user']+"-APPLICATION-"+"KEY"
secret_iv = json_payload['user']+"-APPLICATION-"+"IV"
key_base64 = json_payload['key']
iv_base64 = json_payload['iv']
#print("JSON key = " + key_base64)
#print("JSON IV = " + iv_base64)

#print("secret key = "+ secret_key)
#print("secret iv = "+ secret_iv)
keyVault('set', secret_key, key_base64)
keyVault('set', secret_iv, iv_base64)

