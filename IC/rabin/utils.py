import random
from Crypto.Util.number import *
import codecs
from Crypto.Util.number import getPrime, bytes_to_long, long_to_bytes
from Crypto import Random
import Crypto

# Encuentra la raíz cuadrada cuadrática módulo p donde p ≡ 3 (mod 4)
def sqrt_p_3_mod_4(a, p):
    r = pow(a, (p + 1) // 4, p)
    return r

# Encuentra la raíz cuadrada cuadrática módulo p donde p ≡ 5 (mod 8)
def sqrt_p_5_mod_8(a, p):
    d = pow(a, (p - 1) // 4, p)
    r = 0
    if d == 1:
        r = pow(a, (p + 3) // 8, p)
    elif d == p - 1:
        r = 2 * a * pow(4 * a, (p - 5) // 8, p) % p
    return r

# Implementa el algoritmo extendido de Euclides para encontrar el máximo común divisor (gcd) de dos números
def egcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        gcd, y, x = egcd(b % a, a)
        return gcd, x - (b // a) * y, y

# Realiza la operación de cifrado usando el método propuesto: c = m^2 mod n
def encryption(plaintext, n):
    plaintext = padding(plaintext)
    return plaintext ** 2 % n

# Realiza el relleno de la cadena binaria del texto plano
def padding(plaintext):
    binary_str = bin(plaintext)     # Convierte a una cadena binaria
    output = binary_str + binary_str[-16:]      # Añade los últimos 16 bits al final
    return int(output, 2)       # Convierte de nuevo a entero

# Realiza la operación de descifrado utilizando operaciones modulares
def decryption(a, p, q):
    n = p * q
    r, s = 0, 0

    # Encuentra la raíz cuadrada para p
    if p % 4 == 3:
        r = sqrt_p_3_mod_4(a, p)
    elif p % 8 == 5:
        r = sqrt_p_5_mod_8(a, p)

    # Encuentra la raíz cuadrada para q
    if q % 4 == 3:
        s = sqrt_p_3_mod_4(a, q)
    elif q % 8 == 5:
        s = sqrt_p_5_mod_8(a, q)

    gcd, c, d = egcd(p, q)
    x = (r * d * q + s * c * p) % n
    y = (r * d * q - s * c * p) % n
    lst = [x, n - x, y, n - y]
    print(lst)

    try:
        plaintext = choose(lst)
        string = bin(plaintext)
        string = string[:-16]
        plaintext = int(string, 2)
        return plaintext
    except ValueError as e:
        raise ValueError("Error durante la función de descifrado: {}".format(e))

# Decide qué respuesta elegir comparando los últimos 16 bits de las respuestas posibles
# Devuelve None si no hay ninguna respuesta válida
def choose(lst):
    for i in lst:
        binary = bin(i)
        append = binary[-16:]   # Toma los últimos 16 bits
        binary = binary[:-16]   # Elimina los últimos 16 bits

        if append == binary[-16:]:
            return i
    return None

# Función principal para realizar la operación de cifrado y descifrado
def perform_crypto(msg, bits=60):
    while True:
        p = Crypto.Util.number.getPrime(bits, randfunc=Crypto.Random.get_random_bytes)
        if (p % 4) == 3:
            break

    while True:
        q = Crypto.Util.number.getPrime(bits, randfunc=Crypto.Random.get_random_bytes)
        if (q % 4) == 3:  # Corregido el error, debe ser (q % 4)
            break

    n = p * q

    print("=== Mensaje ===")
    print(("Mensaje=%s") % msg)
    print(("\n=== Clave privada (números primos de %d bits) ===") % bits)
    print(("p=%d, q=%d") % (p, q))

    print("\n=== Clave pública ===")
    print("n=%d" % n)

    plaintext = bytes_to_long(msg.encode('utf-8'))

    ciphertext = encryption(plaintext, n)
    print("\nCifrado:", ciphertext)

    decrypted_text = decryption(ciphertext, p, q)
    st = format(decrypted_text, 'x')
    print("Descifrado:", bytes.fromhex(st).decode())
    return [ciphertext,p,q]

# Función para realizar la operación de descifrado
def perform_decryption(ciphertext, p, q):
    decrypted_text = decryption(ciphertext, p, q)
    st = format(decrypted_text, 'x')
    return bytes.fromhex(st).decode()