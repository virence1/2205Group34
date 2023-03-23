import base_DH
from secretvault import keyVault
from random import randint

# Generate the modulus and base values
p = base_DH.gen_prime(2000, 6000) #modulus
g = base_DH.gen_prime(500, 1000) #base

# Generate Tx private key
Tx_privK = base_DH.gen_prime(1000, 3000)

# Derive Tx public key
Tx_pubK = base_DH.generate_public_key(Tx_privK, p, g)

# Store the modulus, base and Tx public keys to the key vault
keyVault('set', 'pdh', p)
keyVault('set', 'gdh', g)
keyVault('set', 'TxpubKdh', Tx_pubK)

# Debugging purposes
#print("Stored Modulus (p): ", keyVault('get', 'pdh'))
#print("Stored Base (g): ", keyVault('get', 'gdh'))
#print("Stored Tx Public Key: ", keyVault('get', 'TxpubKdh'))

# Store the Tx private key for later retrieval
with open('Tx_privK.txt', 'w') as f:
    f.write(str(Tx_privK))
