import base_DH
from secretvault import keyVault

# Retrieve required variables from key vault (Tx and Rx public keys and p value)
Tx_pubK = keyVault('get', 'TxpubKdh')
Rx_pubK = keyVault('get','RxpubKdh')
p = keyVault('get','pdh')

# Retrieve the Rx private key
f = open('Rx_privK.txt', 'r')
Rx_privK = f.read()

# Derive the Rx secret key
Rx_secretK = base_DH.decode_public_key(int(Tx_pubK), int(Rx_privK), int(p))

# For debugging purposes below
#print(Rx_secretK)
#print(Rx_privK)
