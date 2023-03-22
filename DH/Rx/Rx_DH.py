import base_DH
import math
import requests
from random import randint

#p = base_DH.gen_prime(2000, 6000) #modulus
#g = base_DH.gen_prime(500, 1000) #base
p = get.modulusfromsomewhere
g = get.basefromsomewhere

Rx_privK = base_DH.gen_prime(1000, 3000)

Rx_pubK = base_DH.generate_public_key(Rx_privK, p, g)
key2 = base_DH.decode_public_key(Tx_pubK, Rx_privK, p)

shared_key_Rx = base_DH.decode_public_key(Tx_pubK, Rx_privK, p)
