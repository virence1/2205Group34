from flask import *
import requests
import json
import mysql.connector
import requests
import random
from azure.identity import UsernamePasswordCredential
from azure.keyvault.secrets import SecretClient
from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient
from Crypto.Cipher import AES
from Crypto.Util import Padding
import binascii

app = Flask(__name__)

@app.route("/")
def hello():
    return "<h1 style='color:blue'>Testing Page</h1>"


@app.route("/endpointDestination",methods=['POST'])
def getData():
    payload = request.get_json()
    if payload['combo'] =='132D':
        decrypted_vote = aes_decrypt(payload)
        response = update_votebank(decrypted_vote)
        return "Success 200. Vote captured! "+response

    # Do the db stuff
    return 'Success'


def aes_decrypt(payload):
    # Define the Azure AD tenant ID, client ID, and client secret
    tenant_id = "7fc78b60-eb18-4991-9d0b-1c06abe3f07e"
    client_id = "08477e2d-4d95-41c2-879f-06e0e1a05956"
    client_secret = "3HU8Q~zh9k7VHZA1NknQtEeeSEt7pumb_6MXwa3N"

    # Define the Azure Key Vault URL and secret names
    vault_url = "https://ddd-key-vault.vault.azure.net/"
    secret_iv_name = payload['user'] + "-AES-IV"
    secret_key_name = payload['user'] + "-AES-KEY"
    secret_tag_name = payload['user'] + "-AES-TAG"

    # Create the credential object
    credential = ClientSecretCredential(
        tenant_id=tenant_id,
        client_id=client_id,
        client_secret=client_secret
    )

    # Create the secret client object
    client = SecretClient(vault_url=vault_url, credential=credential)

    # Retrieve the secrets from the key vault
    key_hex = client.get_secret(secret_key_name).value
    iv_hex = client.get_secret(secret_iv_name).value
    tag_hex = client.get_secret(secret_tag_name).value

    # Convert the retrieved values from hex to bytes
    key = binascii.unhexlify(key_hex)
    iv = binascii.unhexlify(iv_hex)
    tag = binascii.unhexlify(tag_hex)

    # Convert the ciphertext from base64 to bytes
    ciphertext_b64 = payload['vote']
    ciphertext = binascii.a2b_base64(ciphertext_b64)

    # Decrypt the ciphertext using the AES key, IV, and tag
    plaintext_str = None  # Initialize the variable here
    cipher = AES.new(key, AES.MODE_GCM, iv)
    try:
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)
        plaintext = Padding.unpad(plaintext, AES.block_size)
        plaintext_str = plaintext.decode('utf-8')
        print("Decrypted vote (Important): ", plaintext_str)
    except ValueError:
        print("Incorrect decryption, vote may have been tampered with")

    # Update the payload with the decrypted message
    if plaintext_str is not None:
        payload['vote'] = plaintext_str
    return payload['vote']


def diffie_decrypt():
    pass

def update_votebank(name):
    mydb = mysql.connector.connect(
        host="localhost", user="dddadmin", password="123456789", database="votebank"
    )
    mycursor = mydb.cursor()
    candidate = name
    sql = "UPDATE votecount SET count = count + 1 WHERE candidate = %s"
    val = (candidate,)
    mycursor.execute(sql, val)
    mydb.commit()
    return "Candidate " + candidate + " vote updated in votebank database."

json_payload = {'vote': 'wv1L37tg/XnCg604TKHRYQ==', 'user': 'X2398754Y', 'combo': '231D', 'nextNode': '3', 'remainingPath': '1D'}
aes_decrypt(json_payload)
print(json_payload)