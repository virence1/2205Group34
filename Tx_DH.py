import math
import requests
from random import randint

def generate_public_key(a, p, g):
    r = (g**a)%p
    return r

def decode_public_key(r_other, a, p):
    key = (r_other**a)%p
    return key

# Encoding alphabets into integers
str_dict = {'a': "690", 'b': "691", 'c': "692", 'd': "693", 'e': "694", 'f': "695", 'g': "696", 'h': "697",
            'i': "698", 'j': "699", 'k': "700", 'l': "701", 'm': "702", 'n': "703", 'o': "704", 'p': "705",
            'q': "706", 'r': "707", 's': "708", 't': "709", 'u': "710", 'v': "711", 'w': "712", 'x': "713",
            'y': "714", 'z': "715", " ": "716", 'A': "717", 'B': "718", 'C': "719", 'D': "720", 'E': "721",
            'F': "722", 'G': "723", 'H': "724", 'I': "725", 'J': "726", 'K': "727", 'L': "728", 'M': "729",
            'N': "730", 'O': "731", 'P': "732", 'Q': "733", 'R': "734", 'S': "735", 'T': "736", 'U': "737",
            'V': "738", 'W': "739", 'X': "740", 'Y': "741", 'Z': "742", ",": "743", ".": "744", "1": "745",
            "2": "746", "3": "747", "4": "748", "5": "749", "6": "750", "7": "751", "8": "752", "9": "753",
            "0": "754",}

# Arbitrary value that increases all the integers above by the stated value. Can be modified
increment_value = 69
for key in str_dict:
    str_dict[key] = str(int(str_dict[key]) + increment_value)

# String encryption
def encrypt_string(string_in, secret_key):
    string_as_num = "".join((str_dict[string_in[n]] for n in range(0,len(string_in))))
    return int(string_as_num) * secret_key

# String decryption
def decrypt_string(encrypted_str, secret_key):
    string_as_num = str(int(encrypted_str // secret_key))
    start_index = 0
    end_index = 3
    string_out = ""
    for _ in range(0, len(string_as_num) // 3):
        string_out += "".join([k for k,v in str_dict.items() if v == string_as_num[start_index:end_index]])
        start_index += 3
        end_index += 3
    return string_out

# Prime number generation
def gen_prime(start, stop):
    mod_list = []
    # Generate list of prime numbers
    for num in range(start, stop):
        if num > 1:
            for i in range(2, num):
                if (num % i) == 0:
                    break
            else:
                mod_list.append(num)
    # Randomise picking of number
    x = randint(1,len(mod_list))
    return mod_list[x]

def DH_algorithm():
    # Generate modulo and base
    p = gen_prime(2000, 6000) # Modulus
    g = gen_prime(500, 1000) # Base
    #print(f"Modulo: {p} \nBase: {g}\n")

    # Private and Public Key generation
    a1 = gen_prime(1000, 3000) # User 1's private key
    r1 = generate_public_key(a1, p, g) # User 1's public key
    a2 = gen_prime(1000, 3000) # User 2's private key
    r2 = generate_public_key(a2, p, g) # User 2's public key


    # User 1 and User 2 - Makes encryption key from the modulus, public key and own private key
    key1 = decode_public_key(r2, a1, p)
    key2 = decode_public_key(r1, a2, p)


    # This should hold true for trust to be established
    if key1 == key2:
        # User 1 - Encrypt and send message to user 2
        data1_in = "This is a test message from User 1 to User 2" # Secret message
		data_encrypted1 = encrypt_string(data1_in, key1) # Encrypts message using the key
        data1 = {"modulo": p, "Tx_publickey": r1, "data": data_encrypted1} # Sets up data packet to send
        return data1
    else:
        print("Incorrect keys.")

def sendToServer(payload):
    url = "http://20.81.124.56/endpointDestination"
    data ={'message':payload}
    response = requests.post(url, json=data)

    if response.status_code == 200:
        print('Message sent successfully >>> ' + str(data))
        print('Message server reply >>> ' + response.text)
    else:
        print('Error sending message: {}'.format(response.text))

    return

payload = DH_algorithm()
sendToServer(payload)
