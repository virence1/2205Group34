import base_DH
from secretvault import keyVault

# Retrieves the public keys and p value from the key vault
Tx_pubK = keyVault('get', 'TxpubKdh')
Rx_pubK = keyVault('get','RxpubKdh')
p = keyVault('get','pdh')

# Reads the private key of the Tx side
f = open('Tx_privK.txt', 'r')
Tx_privK = f.read()

# Derives the secret key from the Tx side
Tx_secretK = base_DH.decode_public_key(int(Rx_pubK), int(Tx_privK), int(p))

# For debugging purposes
#print("Tx secret key: " + str(Tx_secretK))
#print("Tx private key: " + str(Tx_privK))
