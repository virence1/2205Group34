import base_DH
import Rx_getsecretK_DH
from secretvault import keyVault

# Retrieve required variables from key vault (encrypted strings, Tx and Rx public keys and p value)
encryptedtext = keyVault('get', 'Txpayloaddh')

# Call our function to retrieve Rx secret key
Rx_secretK = Rx_getsecretK_DH.Rx_secretK

# Decrypt the string using the secret key. By theory, if the secret key of the Tx and Rx are equivalent to each other, you will obtain the resulting decrypted text
decryptedtext = base_DH.decrypt_string(int(encryptedtext), Rx_secretK)

# Output the decrypted text, for debugging purposes
print(decryptedtext)
