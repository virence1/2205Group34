from Crypto.Cipher import AES
from Crypto.Util import Padding
import binascii
from secretvault import keyVault
from aesupdatemain import aes_encrypt

key_hex = keyVault('get', 'X2398754Y-AES-KEY')
iv_hex = keyVault('get', 'X2398754Y-AES-IV')
tag_hex = keyVault('get', 'X2398754Y-AES-TAG')

key = binascii.unhexlify(key_hex)
iv = binascii.unhexlify(iv_hex)
tag = binascii.unhexlify(tag_hex)

# Call the DH_AES function from aesupdatemain.py to get the ciphertext directly
iv, ciphertext, tag, key = aes_encrypt()
ciphertext_hex = binascii.hexlify(ciphertext).decode('utf-8')

cipher = AES.new(key, AES.MODE_GCM, iv)
try:
    plaintext = cipher.decrypt_and_verify(ciphertext, tag)
    plaintext = Padding.unpad(plaintext, AES.block_size)
    plaintext_str = plaintext.decode('utf-8')
    print("Decrypted message (Important): ", plaintext_str)
except ValueError:
    print("Incorrect decryption, message may have been tampered with")
