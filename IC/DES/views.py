from django.shortcuts import render
import random
from base64 import b64encode, b64decode
from .forms import CryptoForm
from .DES_module import SDES, DDES, TDES  # Reemplaza con el nombre de tu módulo


def get_binary(number, length):
    binary_string = bin(number)[2:]  # Convert to binary and remove '0b' prefix.
    binary_string = binary_string.zfill(length)  # Pad with leading zeros to make it of 'length' bits.
    return binary_string

# Converts an ASCII character to an 8-bit binary string.
def ascii_bin(char):
    block = bin(ord(char))[2:]  # Convert character to binary.
    return "0" * (8 - len(block)) + block  # Pad with zeros to make 8 bits.

# Perform bitwise XOR on two bit strings and return the result.
def xor(str_1, str_2):
    return get_binary(int(str_1, 2) ^ int(str_2, 2), len(str_1))

# Generates an 8-bit Initial Vector (IV) randomly.
def generate_IV():
    IV = get_binary(random.randint(0, 255), 8)
    return IV
    
# Generates a 10-bit random key.
def generate_key():
    K = get_binary(random.randint(0, 255), 10)
    return K
    
# Encrypts text using Electronic Code Book (EBC) mode.
def encrypt_text_EBC(crypto_system, text):
    cipher_text_bits = []
    for char in text:
        block = ascii_bin(char)
        encrypted_block = crypto_system.encrypt(block)
        cipher_text_bits.append(encrypted_block)
    cipher_text_bytes = [int(i, 2).to_bytes(1, byteorder="big") for i in cipher_text_bits]
    return b64encode(b"".join(cipher_text_bytes)).decode()

# Encrypts text using Cipher Block Chaining (CBC) mode.
def encrypt_text_CBC(crypto_system, text, IV):
    cipher_text_bits = []
    if IV == "":
        IV = generate_IV()
    prev_cipher = IV
    for char in text:
        block = ascii_bin(char)
        block = xor(block, prev_cipher)
        encrypted_block = crypto_system.encrypt(block)
        prev_cipher = encrypted_block
        cipher_text_bits.append(encrypted_block)
    cipher_text_bytes = [int(i, 2).to_bytes(1, byteorder="big") for i in cipher_text_bits]
    print(f"IV={IV}")
    return b64encode(b"".join(cipher_text_bytes)).decode()

# Encrypts text using Output Feedback (OFB) mode.
def encrypt_text_OFB(crypto_system, text, IV):
    cipher_text_bits = []
    if IV == "":
        IV = generate_IV()
    prev_output = IV
    for char in text:
        output = crypto_system.encrypt(prev_output)
        block = ascii_bin(char)
        encrypted_block = xor(block, output)
        prev_output = output
        cipher_text_bits.append(encrypted_block)
    cipher_text_bytes = [int(i, 2).to_bytes(1, byteorder="big") for i in cipher_text_bits]
    print(f"IV={IV}")
    return b64encode(b"".join(cipher_text_bytes)).decode()

# Encrypts text using Cipher Feedback (CFB) mode.
def encrypt_text_CFB(crypto_system, text, IV):
    cipher_text_bits = []
    if IV == "":
        IV = generate_IV()
    prev_cipher = IV
    for char in text:
        output = crypto_system.encrypt(prev_cipher)
        block = ascii_bin(char)
        encrypted_block = xor(block, output)
        prev_cipher = encrypted_block
        cipher_text_bits.append(encrypted_block)
    cipher_text_bytes = [int(i, 2).to_bytes(1, byteorder="big") for i in cipher_text_bits]
    print(f"IV={IV}")
    return b64encode(b"".join(cipher_text_bytes)).decode()

# Decrypts text encrypted in Electronic Code Book (EBC) mode.
def decrypt_text_EBC(crypto_system, cipher_text):
    
    cipher_text = [i for i in b64decode(cipher_text)]
    plain_text_bytes = [crypto_system.decrypt(get_binary(i, 8)) for i in cipher_text]
    return "".join([chr(int(i, 2)) for i in plain_text_bytes])

# Decrypts text encrypted in Cipher Block Chaining (CBC) mode.
def decrypt_text_CBC(crypto_system, cipher_text, IV):
    
    cipher_text_bytes = [i for i in b64decode(cipher_text)]
    cipher_text_bits = [get_binary(i, 8) for i in cipher_text_bytes]
    plain_text_bits = []
    prev_cipher = IV
    for i in range(len(cipher_text_bits)):
        decrypted_block = crypto_system.decrypt(cipher_text_bits[i])
        plain_block = xor(decrypted_block, prev_cipher)
        plain_text_bits.append(plain_block)
        prev_cipher = cipher_text_bits[i]
    return "".join([chr(int(i, 2)) for i in plain_text_bits])

# Decrypts text encrypted in Output Feedback (OFB) mode.
def decrypt_text_OFB(crypto_system, cipher_text, IV):
    
    cipher_text_bytes = [i for i in b64decode(cipher_text)]
    cipher_text_bits = [get_binary(i, 8) for i in cipher_text_bytes]
    plain_text_bits = []
    prev_output = IV
    for cipher_block in cipher_text_bits:
        output = crypto_system.encrypt(prev_output)
        plain_block = xor(cipher_block, output)
        plain_text_bits.append(plain_block)
        prev_output = output
    return "".join([chr(int(i, 2)) for i in plain_text_bits])

# Decrypts text encrypted in Cipher Feedback (CFB) mode.
def decrypt_text_CFB(crypto_system, cipher_text, IV):
    
    cipher_text_bytes = [i for i in b64decode(cipher_text)]
    cipher_text_bits = [get_binary(i, 8) for i in cipher_text_bytes]
    plain_text_bits = []
    prev_cipher = IV
    for i in range(len(cipher_text_bits)):
        output = crypto_system.encrypt(prev_cipher)
        plain_block = xor(cipher_text_bits[i], output)
        plain_text_bits.append(plain_block)
        prev_cipher = cipher_text_bits[i]  
    return "".join([chr(int(i, 2)) for i in plain_text_bits])

def encrypt(type_DES,mode,plain_text,K,IV=""):
    if K=="":
        K = generate_key()
  
    if type_DES == "SDES":
        crypto_system = SDES(K)
    elif type_DES == "DDES":
        crypto_system = DDES(K)
    elif type_DES == "TDES":
        crypto_system = TDES(K)

    if mode == "EBC":
        cipher_text = encrypt_text_EBC(crypto_system,plain_text)
    else:
        if IV == "":
            IV = generate_IV()
        if mode == "CBC":
            cipher_text = encrypt_text_CBC(crypto_system,plain_text,IV)
        elif mode == "OFB":
            cipher_text = encrypt_text_OFB(crypto_system,plain_text,IV)
        elif mode == "CFB":
            cipher_text = encrypt_text_CFB(crypto_system,plain_text,IV)
    return cipher_text

def decrypt(type_DES,mode,cipher_text,K,IV=""):
    if type_DES == "SDES":
        crypto_system = SDES(K)
    elif type_DES == "DDES":
        crypto_system = DDES(K)
    elif type_DES == "TDES":
        crypto_system = TDES(K)

    if mode == "EBC":
        plain_text = decrypt_text_EBC(crypto_system,cipher_text)
    elif mode == "CBC":
        plain_text = decrypt_text_CBC(crypto_system,cipher_text,IV)
    elif mode == "OFB":
        plain_text = decrypt_text_OFB(crypto_system,cipher_text,IV)
    elif mode == "CFB":
        plain_text = decrypt_text_CFB(crypto_system,cipher_text,IV)
       
    return plain_text

def crypto_view(request):
    if request.method == 'POST':
        form = CryptoForm(request.POST)
        if form.is_valid():
            operation = form.cleaned_data['operation']
            type_DES = form.cleaned_data['type_DES']
            mode = form.cleaned_data['mode']
            text = form.cleaned_data['text']
            key = form.cleaned_data['key'] or generate_key()  
            IV = form.cleaned_data['IV'] or generate_IV()  
            if operation == 'encrypt':
                result = encrypt(type_DES, mode, text, key, IV)
            else:
                result = decrypt(type_DES, mode, text, key, IV) 
            return render(request, 'result.html', {'result': result})

    else:
        form = CryptoForm()

    return render(request, 'crypto_form.html', {'form': form})
