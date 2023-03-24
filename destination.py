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

@app.route("/")
def hello():
    return "<h1 style='color:blue'>Testing Page</h1>"
	
@app.route("/dh_destPubKey",methods=['POST'])
def receive_message():
    message=request.get_json()
    dh_destPubKey(message)
    return 'Success 200'
	
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
    keyVault('set', RxpubKdh, Rx_pubK)

    # Store the Rx private key locally
    with open('Rx_privK.txt', 'w') as f:
        f.write(str(Rx_privK))
    f.close()
    return 'Store public key to vault'

@app.route("/endpointDestination",methods=['POST'])
def getData():
        payload = request.get_json()
        if payload['combo'] =='132D':
                #decrypted_vote=aes_decrypt(payload)
                decrypted_vote=diffie_decrypt(payload)
                response=update_votebank(decrypted_vote)
                return "Success 200. Vote captured!"+response

        #do the db stuff
        return 'Success'



def aes_decrypt():
        pass

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

    return payload['vote']

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
	
    # Update the payload with the decrypted message
    payload['vote'] = decryptedtext

    return payload['vote']

def update_votebank(name):
        mydb = mysql.connector.connect(
        host="localhost",user="dddadmin",password="123456789",database="votebank")
        mycursor=mydb.cursor()
        candidate=name
        sql = "UPDATE votecount SET votes = votes + 1 WHERE name = %s"
        val=(candidate,)
        mycursor.execute(sql,val)
        mydb.commit()
        return "Record(s) affected is "+str(mycursor.rowcount)
if __name__ == "__main__":
    app.run(host='0.0.0.0')
