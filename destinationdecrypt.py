from Crypto.Cipher import AES                                                                                                                               
from Crypto.Util import Padding
import binascii

key_hex = '59fd85622109aca0b7f1eedf2c348c8a91cc746c9e4ad7889a0b27bc98845855'
iv_hex = '5cfe62522246ee8179a4f329912bd47d'
ciphertext_hex = '12ff4461c303a829c9eb42bfa3837d48cc3579eb17e4acb31dff7979eafccd22'
tag_hex = '00499ca37bc86f30a162d116229fcc58'

key = binascii.unhexlify(key_hex)
iv = binascii.unhexlify(iv_hex)
ciphertext = binascii.unhexlify(ciphertext_hex)
tag = binascii.unhexlify(tag_hex)

cipher = AES.new(key, AES.MODE_GCM, iv)
try:
    plaintext = cipher.decrypt_and_verify(ciphertext, tag)
    plaintext = Padding.unpad(plaintext, AES.block_size)
    plaintext_str = plaintext.decode('utf-8')
    print("Decrypted message: ", plaintext_str)
except ValueError:
    print("Incorrect decryption, message may have been tampered with")
