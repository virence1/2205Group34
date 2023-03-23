from Crypto.Cipher import AES
from Crypto.Util import Padding
import binascii
from secretvault import keyVault


def aes_decrypt(payload):
    key_hex = keyVault('get', 'X2398754Y-AES-KEY')
    iv_hex = keyVault('get', 'X2398754Y-AES-IV')
    tag_hex = keyVault('get', 'X2398754Y-AES-TAG')

    key = binascii.unhexlify(key_hex)
    iv = binascii.unhexlify(iv_hex)
    tag = binascii.unhexlify(tag_hex)

    ciphertext_b64 = payload['vote']
    ciphertext = binascii.a2b_base64(ciphertext_b64)

    cipher = AES.new(key, AES.MODE_GCM, iv)
    try:
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)
        plaintext = Padding.unpad(plaintext, AES.block_size)
        plaintext_str = plaintext.decode('utf-8')
        print("Decrypted vote (Important): ", plaintext_str)
    except ValueError:
        print("Incorrect decryption, vote may have been tampered with")


if __name__ == '__main__':
    # Example usage:
    payload = {'message': 'Abcp', 'nextNode': 'D', 'remainingPath': '1,3,D', 'vote': 'cL/f3MvnLTC4yp8HTpumpA=='}
    aes_decrypt(payload)
