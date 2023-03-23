import base_DH
import math
import base64
import binascii
import requests
from secretvault import keyVault
from random import randint

Tx_pubK = keyVault('get', 'TxpubKdh')
Rx_pubK = keyVault('get','RxpubKdh')
p = keyVault('get','pdh')

f = open('Tx_privK.txt', 'r')
Tx_privK = f.read()
Tx_secretK = base_DH.decode_public_key(int(Rx_pubK), int(Tx_privK), int(p))
print(Tx_secretK)
print(Tx_privK)
