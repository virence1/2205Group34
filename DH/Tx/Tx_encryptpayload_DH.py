import base_DH
import Tx_getsecretK_DH
from secretvault import keyVault

# "plaintext" variable is to be replaced with the relevant code during integration
plaintext = "insertthejsontextstringhere"

# Encrypts the above variable with our derived secret code
encryptedtext = base_DH.encrypt_string(plaintext, Tx_getsecretK_DH.Tx_secretK)

# Stores the encrypted payload into the key vault
keyVault('set','Txpayloaddh', encryptedtext)

# Erases the private key as we are done with it's usage
f = open('Tx_privK.txt', 'w')
f.write('')