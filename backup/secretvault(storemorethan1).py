import requests
import random
from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient

def keyVault(mode, secret_value_to_store=None):
    tenant_id = "7fc78b60-eb18-4991-9d0b-1c06abe3f07e"
    client_id = "08477e2d-4d95-41c2-879f-06e0e1a05956"
    client_secret = "3HU8Q~zh9k7VHZA1NknQtEeeSEt7pumb_6MXwa3N"

    vault_url = "https://ddd-key-vault.vault.azure.net/"
    secret_name = "testing"
    #to store extra secret
    secret_name1= "testing1"
    
    credential = ClientSecretCredential(
        tenant_id=tenant_id,
        client_id=client_id,
        client_secret=client_secret
    )

    client = SecretClient(vault_url=vault_url, credential=credential)

    if mode == 'set':
        client.set_secret(secret_name, secret_value_to_store)
        #to store extra secret
        client.set_secret(secret_name1, secret_value_to_store)
        return "Secret stored successfully."

    elif mode == 'get':
        secret_value = client.get_secret(secret_name).value
        #to store extra secret
        secret_value2 = client.get_secret(secret_name1).value
        return secret_value,secret_value2

    else:
        return "Invalid mode. Use 'set' or 'get'."


# Store a new secret value in the Key Vault
store_result = keyVault('set', 'hello')
print(store_result)

# Retrieve the secret value from the Key Vault to confirm it has been stored successfully
secret_value = keyVault('get')
#to store extra secret
secret_value2=keyVault('get')
#to store extra secret
print(secret_value)
print(secret_value2)
