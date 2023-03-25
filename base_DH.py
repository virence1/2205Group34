# Base helper functions for the Diffie-Hellman key exchange algorithm
from random import randint

# Generate a public key
def generate_public_key(a, p, g):
    r = (g**a)%p
    return r

# Decode the specific public key
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
            "0": "754", "=": "755", "/": "756", "+": "757", "-": "758"}

# Arbitrary value that increases all the integers above by the stated value. Can be modified if needed
increment_value = 69
for key in str_dict:
    str_dict[key] = str(int(str_dict[key]) + increment_value)

# Encrypt the string with the secret ke
def encrypt_string(string_in, secret_key):
    string_as_num = "".join((str_dict[string_in[n]] for n in range(0,len(string_in))))
    return int(string_as_num) * secret_key

# Decrypt the string with the secret key
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

# Generate a prime number ranging from the "start" value to the "stop" value
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
