from .DES_module import SDES,DDES, TDES
import random
import numpy as np
from io import BytesIO
from PIL import Image

def get_binary(number, length):
    # Converts an integer to a binary string of specified length.
    binary_string = bin(number)[2:]  # Convert to binary and remove '0b'
    binary_string = binary_string.zfill(length)  # Pad with zeros to required length
    return binary_string

def xor(str_1, str_2):
    # Perform bitwise XOR on two binary strings.
    return get_binary(int(str_1, 2) ^ int(str_2, 2), len(str_1))

def generate_IV():
    # Generates an 8-bit random Initial Vector.
    IV = get_binary(random.randint(0, 255), 8)
    return IV

def generate_key():
    # Generates a 10-bit random key.
    K = get_binary(random.randint(0, 1023), 10)  # Corrected the upper limit for 10 bits
    return K

# Encryption and decryption functions for image data:

def encrypt_image_EBC(crypto_system, bytes):
    # Encrypts image data in Electronic Code Book mode.
    cipher_bytes = []
    for byte in bytes:
        encrypted_block = crypto_system.encrypt(get_binary(byte, 8))
        cipher_bytes.append(encrypted_block)
    cipher_bytes = [int(i, 2).to_bytes(1, byteorder="big") for i in cipher_bytes]
    return b"".join(cipher_bytes)

def encrypt_image_CBC(crypto_system, bytes,IV):
    # Encrypts image data in Electronic Code Book mode.
    cipher_bytes = []
    prev_cipher = IV
    for byte in bytes:
        block = get_binary(byte, 8)
        block = xor(block,prev_cipher)
        encrypted_block = crypto_system.encrypt(block)
        prev_cipher = encrypted_block
        cipher_bytes.append(encrypted_block)
    cipher_bytes = [int(i, 2).to_bytes(1, byteorder="big") for i in cipher_bytes]
    return b"".join(cipher_bytes)

def encrypt_image_CFB(crypto_system, bytes,IV):
    # Encrypts image data in Electronic Code Book mode.
    cipher_bytes = []
    prev_cipher = IV
    for byte in bytes:
        output = crypto_system.encrypt(prev_cipher)
        block = get_binary(byte, 8)
        encrypted_block = xor(block,output)
        prev_cipher = encrypted_block
        cipher_bytes.append(encrypted_block)
    cipher_bytes = [int(i, 2).to_bytes(1, byteorder="big") for i in cipher_bytes]
    return b"".join(cipher_bytes)

def encrypt_image_OFB(crypto_system, bytes,IV):
    # Encrypts image data in Electronic Code Book mode.
    cipher_bytes = []
    prev_output = IV
    for byte in bytes:
        output = crypto_system.encrypt(prev_output)
        block = get_binary(byte, 8)
        encrypted_block = xor(block,output)
        prev_output = output
        cipher_bytes.append(encrypted_block)
    cipher_bytes = [int(i, 2).to_bytes(1, byteorder="big") for i in cipher_bytes]
    return b"".join(cipher_bytes)

# Main encryption and decryption process for images:
def encrypt_image(type_DES, mode, img_bytes, K, IV=""):
    if type_DES == "SDES":
        crypto_system = SDES(K)
    elif type_DES == "DDES":
        crypto_system = DDES(K)
    elif type_DES == "TDES":
        crypto_system = TDES(K)

    if mode == "EBC":
        encrypted_bytes = encrypt_image_EBC(crypto_system, img_bytes)
    else:
        if IV == "":
            IV = generate_IV()
        if mode == "CBC":
            encrypted_bytes = encrypt_image_CBC(crypto_system,img_bytes,IV)
        if mode == "CFB":
            encrypted_bytes = encrypt_image_CFB(crypto_system,img_bytes,IV)
        if mode == "OFB":
            encrypted_bytes = encrypt_image_OFB(crypto_system,img_bytes,IV)

    return encrypted_bytes

def decrypt_image_EBC(crypto_system, img_bytes):
    # Decrypts image data in Electronic Code Book mode.
    decrypted_bytes = []
    for byte in img_bytes:
        decrypted_block = crypto_system.decrypt(get_binary(byte, 8))
        decrypted_bytes.append(decrypted_block)
    return b"".join([int(i, 2).to_bytes(1, byteorder="big") for i in decrypted_bytes])

def decrypt_image_CBC(crypto_system, img_bytes, IV):
    # Decrypts image data in Cipher Block Chaining mode.
    decrypted_bytes = []
    prev_cipher = IV
    for byte in img_bytes:
        decrypted_block = crypto_system.decrypt(get_binary(byte, 8))
        block = xor(decrypted_block, prev_cipher)
        prev_cipher = get_binary(byte, 8)
        decrypted_bytes.append(block)
    return b"".join([int(i, 2).to_bytes(1, byteorder="big") for i in decrypted_bytes])

def decrypt_image_CFB(crypto_system, img_bytes, IV):
    # Decrypts image data in Cipher Feedback mode.
    decrypted_bytes = []
    prev_cipher = IV
    for byte in img_bytes:
        output = crypto_system.encrypt(prev_cipher)
        decrypted_block = xor(get_binary(byte, 8), output)
        prev_cipher = get_binary(byte, 8)
        decrypted_bytes.append(decrypted_block)
    return b"".join([int(i, 2).to_bytes(1, byteorder="big") for i in decrypted_bytes])

def decrypt_image_OFB(crypto_system, img_bytes, IV):
    # Decrypts image data in Output Feedback mode.
    decrypted_bytes = []
    prev_output = IV
    for byte in img_bytes:
        output = crypto_system.encrypt(prev_output)
        decrypted_block = xor(get_binary(byte, 8), output)
        prev_output = output
        decrypted_bytes.append(decrypted_block)
    return b"".join([int(i, 2).to_bytes(1, byteorder="big") for i in decrypted_bytes])


def decrypt_image(type_DES,mode,img_bytes, K,IV=""):
    if type_DES == "SDES":
        crypto_system = SDES(K)
    elif type_DES == "DDES":
        crypto_system = DDES(K)
    elif type_DES == "TDES":
        crypto_system = TDES(K)
    if mode == "EBC":
        decrypted_bytes = encrypt_image_EBC(crypto_system, img_bytes)
    else:
        if IV == "":
            IV = generate_IV()
        if mode == "CBC":
            decrypted_bytes = decrypt_image_CBC(crypto_system,img_bytes,IV)
        if mode == "CFB":
            decrypted_bytes = decrypt_image_CFB(crypto_system,img_bytes,IV)
        if mode == "OFB":
            decrypted_bytes = decrypt_image_OFB(crypto_system,img_bytes,IV)
    
    return decrypted_bytes
