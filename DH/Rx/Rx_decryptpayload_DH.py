import base_DH
import math
import base64
import binascii
import requests
import Rx_getsecretK_DH
from secretvault import keyVault
from random import randint

encryptedtext = keyVault('get', 'Txpayloaddh')
Tx_pubK = keyVault('get', 'TxpubKdh')
Rx_pubK = keyVault('get','RxpubKdh')
p = keyVault('get','pdh')

f = open('Rx_privK.txt', 'r')
Rx_privK = f.read()

Rx_secretK = base_DH.decode_public_key(int(Tx_pubK), int(Rx_privK), int(p))

decryptedtext = base_DH.decrypt_string(int(encryptedtext), Rx_secretK)

print(decryptedtext)
