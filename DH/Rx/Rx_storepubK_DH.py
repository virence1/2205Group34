import base_DH
import math
import base64
import binascii
import requests
from secretvault import keyVault
from random import randint

#print("Retrieved stored Modulus: ", keyVault('get', 'pdh'))
#print("Retrieved stored Base: ", keyVault('get', 'gdh'))
#print("Retrieved stored Tx Public Key: ", keyVault('get', 'TxpubKdh'))

p = keyVault('get', 'pdh')
g = keyVault('get', 'gdh')
Tx_pubK = keyVault('get', 'TxpubKdh')

Rx_privK = base_DH.gen_prime(1000, 3000)
Rx_pubK = base_DH.generate_public_key(Rx_privK, int(p), int(g))
keyVault('set','RxpubKdh', Rx_pubK)

with open('Rx_privK.txt', 'w') as f:
    f.write(str(Rx_privK))
