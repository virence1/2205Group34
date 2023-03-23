import base_DH
import math
import base64
import binascii
import requests
from secretvault import keyVault
from random import randint

p = base_DH.gen_prime(2000, 6000) #modulus
g = base_DH.gen_prime(500, 1000) #base

Tx_privK = base_DH.gen_prime(1000, 3000)
Tx_pubK = base_DH.generate_public_key(Tx_privK, p, g)


keyVault('set', 'pdh', p)
keyVault('set', 'gdh', g)
keyVault('set', 'TxpubKdh', Tx_pubK)

print("Stored Modulus: ", keyVault('get', 'pdh'))
print("Stored Base: ", keyVault('get', 'gdh'))
print("Stored Tx Public Key: ", keyVault('get', 'TxpubKdh'))

with open('Tx_privK.txt', 'w') as f:
    f.write(str(Tx_privK))
