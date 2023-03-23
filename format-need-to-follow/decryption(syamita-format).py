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

@app.route("/")
def hello():
    return "<h1 style='color:blue'>Testing Page</h1>"


@app.route("/endpointDestination",methods=['POST'])
def getData():
        payload = request.get_json()
        #if payload['combo'] =='132D':
                #decrypted_vote=aes_decrypt(payload)
                #response=update_votebank(decrypted_vote)
                #return "Success 200. Vote captured!"+response

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

def diffie_decrypt():
        pass

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
