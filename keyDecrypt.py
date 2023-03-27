import requests
import random
import json
import base64
import binascii
from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient

from Crypto.Cipher import AES
from Crypto.Util import Padding

def finalDecrypt(payload):

    #Grabbing only the vote:
    application_encrypted_vote = payload['vote']
    account_user = payload['user']

    #Grabbing stuff from keyVault
    tenant_id = "7fc78b60-eb18-4991-9d0b-1c06abe3f07e"
    client_id = "08477e2d-4d95-41c2-879f-06e0e1a05956"
    client_secret = "3HU8Q~zh9k7VHZA1NknQtEeeSEt7pumb_6MXwa3N"

    vault_url = "https://ddd-key-vault.vault.azure.net/"
    application_key = account_user + "-APPLICATION-" + "KEY"
    application_iv = account_user + "-APPLICATION-" + "IV"

    credential = ClientSecretCredential(
        tenant_id=tenant_id,
        client_id=client_id,
        client_secret=client_secret
    )
    client = SecretClient(vault_url=vault_url, credential=credential)
    
    # Retrieve the secrets from the key vault
    key_hex = client.get_secret(application_key).value
    iv_hex = client.get_secret(application_iv).value

    # Convert the retrieved values from base to bytes
    key = binascii.a2b_base64(key_hex)
    iv = binascii.a2b_base64(iv_hex)
    ciphertext = binascii.a2b_base64(application_encrypted_vote)


    cipher = AES.new(key, AES.MODE_CBC, iv)
    try:
        plaintext = cipher.decrypt(ciphertext)
        plaintext = Padding.unpad(plaintext, AES.block_size)
        plaintext_str = plaintext.decode('utf-8')
        print("Decrypted vote (Important): ", plaintext_str)
    except ValueError:
        print("Incorrect decryption, vote may have been tampered with")

    # Update the payload with the decrypted message
    payload['vote'] = plaintext_str
    return payload['vote']


json_payload = {"vote": "yourencryptedvotehere", "user": "yourusernamehere", "combo": "213D", "nextNode": "1", "remainingPath": "3D"}
#json_data = json.loads(json_payload)

finalDecrypt(json_payload)
print("Decrypted JSON: " + str(json_payload))