from flask import *
import requests
import json
app = Flask(__name__)
import mysql.connector
import requests
import random
from azure.identity import UsernamePasswordCredential
from azure.keyvault.secrets import SecretClient
from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
import textwrap
import base64
import base_DH
from secretvault import keyVault
from random import randint
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from Crypto.Util import Padding
import hmac
import json
import hashlib
import binascii

@app.route("/")
def hello():
    return "<h1 style='color:blue'>Testing Page</h1>"
	
@app.route("/loading",methods=['POST'])
def receive_message():
    message = request.get_json()
    dh_destPubKey(message)
    return '32'
	
def dh_destPubKey(payload):
    # Get Tx public key, p and g value from the key vault
    pdh = payload['user']+"-"+"DIFFIEHELLMAN"+"-MODULUS"
    gdh = payload['user']+"-"+"DIFFIEHELLMAN"+"-BASE"
    p = keyVault('get', pdh)
    g = keyVault('get', gdh)

    # Generate Rx private key
    Rx_privK = base_DH.gen_prime(1000, 3000)

    # Derive the Rx public key
    Rx_pubK = base_DH.generate_public_key(Rx_privK, int(p), int(g))

    # Store Rx public key in key vault
    RxpubKdh = payload['user']+"-"+"DIFFIEHELLMAN"+"-RXPUBLICKEY"
    keyVault('set',RxpubKdh, Rx_pubK)

    # Store the Rx private key locally
    with open('Rx_privK.txt', 'w') as f:
        f.write(str(Rx_privK))
    f.close()

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
            
@app.route("/endpointDestination",methods=['POST'])

def getData():
        payload = request.get_json()
        result=verify_digest(payload)
        if result == True:
            if payload['combo'] == "ZPBGW":
                first_layer = diffie_decrypt(payload)
                second_layer = aes_decrypt(first_layer)
                third_layer = rsa_decrypt(second_layer)
                fourth_layer = live_decrypt(third_layer)
                db_result = update_votebank(fourth_layer['vote'])
                return "40"+db_result
            elif payload['combo'] == "ZPGBW" :
                first_layer = aes_decrypt(payload)
                second_layer = diffie_decrypt(first_layer)
                third_layer = rsa_decrypt(second_layer)
                fourth_layer = live_decrypt(third_layer)
                db_result = update_votebank(fourth_layer['vote'])
                return "40"+db_result
            elif payload['combo'] == "ZBGPW" :
                first_layer = rsa_decrypt(payload)
                second_layer = diffie_decrypt(first_layer)
                third_layer = aes_decrypt(second_layer)
                fourth_layer = live_decrypt(third_layer)
                db_result = update_votebank(fourth_layer['vote'])
                return "40"+db_result
            elif payload['combo'] == "ZBPGW" :
                first_layer = diffie_decrypt(payload)
                second_layer = rsa_decrypt(first_layer)
                third_layer = aes_decrypt(second_layer)
                fourth_layer = live_decrypt(third_layer)
                db_result = update_votebank(fourth_layer['vote'])
                return "40"+db_result
            elif payload['combo'] == "ZGPBW" :
                first_layer = aes_decrypt(payload)
                second_layer = rsa_decrypt(first_layer)
                third_layer = diffie_decrypt(second_layer)
                fourth_layer = live_decrypt(third_layer)
                db_result = update_votebank(fourth_layer['vote'])
                return "40"+db_result
            elif payload['combo'] == "ZGBPW" :
                first_layer = rsa_decrypt(payload)
                second_layer = aes_decrypt(first_layer)
                third_layer = diffie_decrypt(second_layer)
                fourth_layer = live_decrypt(third_layer)
                db_result = update_votebank(fourth_layer['vote'])
                return "40"+db_result
                
                
            
        else:
            return 'NOUWU'


def aes_decrypt(payload):
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

    # Retrieve the secret key and IV from the Azure Key Vault
    secret_key_name = payload['user'] + "-AES-KEY"
    secret_iv_name = payload['user'] + "-AES-IV"
    key_secret = client.get_secret(secret_key_name)
    iv_secret = client.get_secret(secret_iv_name)

    # Decode the base64-encoded key and IV
    key_bytes = base64.b64decode(key_secret.value)
    iv_bytes = base64.b64decode(iv_secret.value)

    # Use the decoded key and IV to create a new AES cipher object in CBC mode
    cipher = AES.new(key_bytes, AES.MODE_CBC, iv_bytes)

    # Decode the base64-encoded ciphertext from the payload
    ciphertext = base64.b64decode(payload['vote'])

     # Use the cipher object to decrypt the ciphertext
    decrypted_data = cipher.decrypt(ciphertext)

    # Unpad the decrypted plaintext
    plaintext = unpad(decrypted_data, AES.block_size)

    decoded_data = plaintext.decode('utf-8')

    payload['vote'] = decoded_data

    # Return the decrypted plaintext
    return payload


def rsa_decrypt(payload):
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

    secretname=payload['user']+"-"+"RSA"+"-PRIVATEKEY"

    # Retrieve the private key from the key vault
    private_key_str = client.get_secret(secretname).value.encode('utf-8')
    private_key_bytes = bytes(private_key_str)


    private_key = serialization.load_pem_private_key(
        private_key_bytes,
        password=None,
    )
    print("Private key retrieved from Key Vault.")
    # Decode the encrypted message from hex string
    encrypted_message = bytes.fromhex(payload['vote'])
    decrypted_message = private_key.decrypt(
    encrypted_message,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None,
    ),
)

    # Decrypt the message using the private key
    decrypted_message = private_key.decrypt(
        encrypted_message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # Update the payload with the decrypted message
    payload['vote'] = decrypted_message.decode('utf-8')

    return payload

def diffie_decrypt(payload):
    # Retrieve required variables from key vault (encrypted strings, Tx and Rx public keys and p value)
    Txpayloaddh = payload['user']+"-"+"DIFFIEHELLMAN"+"-TXPAYLOAD"
    encryptedtext = keyVault('get', Txpayloaddh)
	
    # Retrieve required variables from key vault (Tx and Rx public keys and p value)
    TxpubKdh = payload['user']+"-"+"DIFFIEHELLMAN"+"-TXPUBLICKEY"
    pdh = payload['user']+"-"+"DIFFIEHELLMAN"+"-MODULUS"
    Tx_pubK = keyVault('get', TxpubKdh)
    p = keyVault('get',pdh)

    # Retrieve the Rx private key
    f = open('Rx_privK.txt', 'r')
    Rx_privK = f.read()
    f.close()

    # Derive the Rx secret key
    Rx_secretK = base_DH.decode_public_key(int(Tx_pubK), int(Rx_privK), int(p))
	
    # Decrypt the string using the secret key. By theory, if the secret key of the Tx and Rx are equivalent to each other, you will obtain the resulting decrypted text
    decryptedtext = base_DH.decrypt_string(int(encryptedtext), Rx_secretK)

    # Erases the private key as we are done with it's usage
    f = open('Rx_privK.txt', 'w')
    f.write('')
    f.close()

    # Output the decrypted text, for debugging purposes
    print(decryptedtext)
	
    # Update the payload with the decrypted message
    payload['vote'] = decryptedtext

    return payload

def live_decrypt(payload):

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
    return payload



def update_votebank(name):
        mydb = mysql.connector.connect(
        host="localhost",user="dddadmin",password="123456789",database="votebank")
        mycursor=mydb.cursor()
        candidate=name
        sql = "UPDATE votecount SET votes = votes + 1 WHERE name = %s"
        val=(candidate,)
        mycursor.execute(sql,val)
        mydb.commit()
        return "50"
if __name__ == "__main__":
    app.run(host='0.0.0.0')
