import base_DH
import math
import base64
import binascii
import requests
import Tx_getsecretK_DH
from secretvault import keyVault
from random import randint

plaintext = "thisisatestplshelp"
encryptedtext = base_DH.encrypt_string(plaintext, Tx_getsecretK_DH.Tx_secretK)

keyVault('set','Txpayloaddh', encryptedtext)