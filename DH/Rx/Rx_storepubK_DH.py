import base_DH
from secretvault import keyVault
from random import randint

# For debugging purposes
#print("Retrieved stored Modulus: ", keyVault('get', 'pdh'))
#print("Retrieved stored Base: ", keyVault('get', 'gdh'))
#print("Retrieved stored Tx Public Key: ", keyVault('get', 'TxpubKdh'))

# Get Tx public key, p and g value from the key vault
p = keyVault('get', 'pdh')
g = keyVault('get', 'gdh')
Tx_pubK = keyVault('get', 'TxpubKdh')


# Generate Rx private key
Rx_privK = base_DH.gen_prime(1000, 3000)

# Derive the Rx public key
Rx_pubK = base_DH.generate_public_key(Rx_privK, int(p), int(g))

# Store Rx public key in key vault
keyVault('set','RxpubKdh', Rx_pubK)

# Store the Rx private key locally
with open('Rx_privK.txt', 'w') as f:
    f.write(str(Rx_privK))
