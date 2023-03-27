from flask import Flask , request
import requests
import logging
from logging.handlers import RotatingFileHandler
import json
import base_DH
import hmac
import hashlib
from secretvault import keyVault
from random import randint

app = Flask(__name__)

@app.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"
	
def sendToNode1(message):
    url = "http://20.81.121.55/endpoint1"
    response = requests.post(url, json=message)
    if response.status_code == 200:
        return "10" + response.text
    else:
        return "60"

def sendToNode2(message):
    url = "http://20.106.233.101/endpoint2"
    response = requests.post(url, json=message)
    if response.status_code == 200:
        return "20" + response.text
    else:
        return "70"

def sendToDestination(message):
    url = "http://20.81.124.56/endpointDestination"
    response = requests.post(url, json=message)
    if response.status_code == 200:
        return "40" + response.text
    else:
        return "90"        

def hash_payload(payload):
    # Compute the HMAC-SHA256 digest of the payload using the secret key
    secret_key = keyVault('get', "tamper-secret")
    payload_str = json.dumps(payload)  # convert the dictionary to a string
    digest = hmac.new(secret_key.encode(), msg=payload_str.encode('utf-8'), digestmod=hashlib.sha256).hexdigest()
    keyVault('set', "PAYLOAD-NODE3-DIGEST", digest)
    return payload

def verify_digest(payload):
    if payload['prevNode'] == 'Z':
        secret_key = keyVault('get', "tamper-secret")
        prev_node_digest = keyVault('get', "PAYLOAD-LIVE-DIGEST")
        payload_str = json.dumps(payload)
        computed_digest = hmac.new(secret_key.encode(), msg=payload_str.encode('utf-8'), digestmod=hashlib.sha256).hexdigest()
        if computed_digest == prev_node_digest:
            return True
        else:
            return False
    elif payload['prevNode'] == 'P':
        secret_key = keyVault('get', "tamper-secret")
        prev_node_digest = keyVault('get', "PAYLOAD-NODE1-DIGEST")
        payload_str = json.dumps(payload)
        computed_digest = hmac.new(secret_key.encode(), msg=payload_str.encode('utf-8'), digestmod=hashlib.sha256).hexdigest()
        if computed_digest == prev_node_digest:
            return True
        else:
            return False
    elif payload['prevNode'] == 'B':
        secret_key = keyVault('get', "tamper-secret")
        prev_node_digest = keyVault('get', "PAYLOAD-NODE2-DIGEST")
        payload_str = json.dumps(payload)
        computed_digest = hmac.new(secret_key.encode(), msg=payload_str.encode('utf-8'), digestmod=hashlib.sha256).hexdigest()
        if computed_digest == prev_node_digest:
            return True
        else:
            return False
    elif payload['prevNode'] == 'G':
        secret_key = keyVault('get', "tamper-secret")
        prev_node_digest = keyVault('get', "PAYLOAD-NODE3-DIGEST")
        payload_str = json.dumps(payload)
        computed_digest = hmac.new(secret_key.encode(), msg=payload_str.encode('utf-8'), digestmod=hashlib.sha256).hexdigest()
        if computed_digest == prev_node_digest:
            return True
        else:
            return False
 
@app.route("/endpoint3",methods=['POST'])
def receive_message():
    message=request.get_json()
    result=verify_digest(message)
    if result == True:
        dh_n3PubKey(message)
        intermediate_response=dh_destPubKey(message)
        encrypted_message = dh_encrypt(message)
        nextNode = encrypted_message['remainingPath'][0]
        if nextNode == 'B':
            updatedPathLeft = encrypted_message['remainingPath'][1:]
            encrypted_message['remainingPath'] = updatedPathLeft
            encrypted_message['prevNode'] = 'G'
            hashed_payload=hash_payload(encrypted_message)
            response = sendToNode2(hashed_payload)
            return "30UWU"+intermediate_response+response
        elif nextNode == 'P':
            updatedPathLeft = encrypted_message['remainingPath'][1:]
            encrypted_message['remainingPath'] = updatedPathLeft
            encrypted_message['prevNode'] = 'G'
            hashed_payload=hash_payload(encrypted_message)
            response = sendToNode1(hashed_payload)
            return "30UWU"+intermediate_response+response
        elif nextNode == 'W':
            updatedPathLeft = encrypted_message['remainingPath'][1:]
            encrypted_message['remainingPath'] = updatedPathLeft
            encrypted_message['prevNode'] = 'G'
            hashed_payload=hash_payload(encrypted_message)
            response = sendToDestination(hashed_payload)
            return "30UWU"+intermediate_response+response
        elif nextNode == 'G':
            return "80UWU"
    else:
        return "NOUWU"
	
def dh_n3PubKey(payload):
    # Generate the modulus and base values
    p = base_DH.gen_prime(2000, 6000) #modulus
    g = base_DH.gen_prime(500, 1000) #base

    # Generate Tx private key
    Tx_privK = base_DH.gen_prime(1000, 3000)

    # Derive Tx public key
    Tx_pubK = base_DH.generate_public_key(Tx_privK, p, g)

    # Store the modulus, base and Tx public keys to the key vault
    pdh = payload['user']+"-"+"DIFFIEHELLMAN"+"-MODULUS"
    gdh = payload['user']+"-"+"DIFFIEHELLMAN"+"-BASE"
    TxpubKdh = payload['user']+"-"+"DIFFIEHELLMAN"+"-TXPUBLICKEY"
    keyVault('set', pdh, p)
    keyVault('set', gdh, g)
    keyVault('set', TxpubKdh, Tx_pubK)

    # Store the Tx private key for later retrieval
    with open('Tx_privK.txt', 'w') as f:
        f.write(str(Tx_privK))
    f.close()

def dh_destPubKey(message):
    url = "http://20.81.124.56/loading"
    response = requests.post(url, json=message)
    if response.status_code == 200:
        return "32" + response.text
    else:
        return "82"

def dh_encrypt(payload):		
    # Retrieves the public keys and p value from the key vault
    RxpubKdh = payload['user']+"-"+"DIFFIEHELLMAN"+"-RXPUBLICKEY"
    pdh = payload['user']+"-"+"DIFFIEHELLMAN"+"-MODULUS"
    Rx_pubK = keyVault('get', RxpubKdh)
    p = keyVault('get',pdh)

    # "plaintext" variable is to be replaced with the relevant code during integration
    plaintext = payload['vote']
	
    # Reads the private key of the Tx side
    f = open('Tx_privK.txt', 'r')
    Tx_privK = f.read()
    f.close()

    # Derives the secret key from the Tx side
    Tx_secretK = base_DH.decode_public_key(int(Rx_pubK), int(Tx_privK), int(p))

    # Encrypts the above variable with our derived secret code
    encryptedtext = base_DH.encrypt_string(plaintext, Tx_secretK)

    # Stores the encrypted payload into the key vault
    Txpayloaddh = payload['user']+"-"+"DIFFIEHELLMAN"+"-TXPAYLOAD"
    keyVault('set', Txpayloaddh, encryptedtext)

    # Erases the private key as we are done with it's usage
    f = open('Tx_privK.txt', 'w')
    f.write('')
    f.close()

    payload['vote'] = str(encryptedtext)
    return payload

if __name__ == "__main__":
    app.run(host='0.0.0.0')
