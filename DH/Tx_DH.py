import base_DH
import math
import requests
from random import randint

p = base_DH.gen_prime(2000, 6000) #modulus
g = base_DH.gen_prime(500, 1000) #base

Tx_privK = base_DH.gen_prime(1000, 3000)
Tx_pubK = base_DH.generate_public_key(Tx_privK, p, g)
