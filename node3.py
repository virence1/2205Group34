from flask import Flask , request
import requests
import logging
from logging.handlers import RotatingFileHandler
import json
import base_DH
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
        return "Node 3 received | " + response.text
        print('Message sent successfully')
    else:
        return('Error sending message to Node 1 : {}'.format(response.text))

def sendToNode2(message):
    url = "http://20.106.233.101/endpoint2"
    response = requests.post(url, json=message)
    if response.status_code == 200:
        return "Node 3 received | " + response.text
        print('Message sent successfully')
    else:
        return ('Error sending message to Node 2 : {}'.format(response.text))

def sendToDestination(message):
    url = "http://20.81.124.56/endpointDestination"
    response = requests.post(url, json=message)
    if response.status_code == 200:
        return "Node 3 received | " + response.text
        print('Message sent successfully')
    else:
        return ('Error sending message to Destination : {}'.format(response.text))


@app.route("/endpoint3",methods=['POST'])
def receive_message():
    message=request.get_json()
    dh_n3PubKey(message)
    dh_destPubKey(message)
    encrypted_message=dh_encrypt(message)
    if encrypted_message['nextNode'] == '1':
        pathLeft = encrypted_message['remainingPath']
        newpathLeft = pathLeft[1:]
        response = sendToNode1(encrypted_message)
        return response
	
    elif encrypted_message['nextNode'] == '2':
        pathLeft = encrypted_message['remainingPath']
        newpathLeft = pathLeft[1:]
        response = sendToNode2(encrypted_message)
        return response

    elif encrypted_message['nextNode'] == 'D':
        encrypted_message['remainingPath'] = "NULL"
        response = sendToDestination(encrypted_message)
        return response
		
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
    url = "http://20.81.124.56/dh_destPubKey"
    response = requests.post(url, json=message)
    if response.status_code == 200:
        return "Node 3 received | " + response.text
        print('Message sent successfully')
    else:
        return ('Error sending message to Destination : {}'.format(response.text))

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
	
    payload['vote'] = encryptedtext
    return payload

if __name__ == "__main__":
    app.run(host='0.0.0.0')
