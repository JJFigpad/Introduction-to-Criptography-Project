# Función para cifrar un texto usando el cifrado de Vigenère

def vigenere_cipher(text, key):
    encrypted_text = ""  # Inicializa la variable para almacenar el texto cifrado
    key_length = len(key)  # Obtiene la longitud de la clave

    # Itera a través de cada carácter del texto a cifrar
    for i in range(len(text)):
        char = text[i]  # Obtiene un carácter del texto

        # Verifica si el carácter es una letra del alfabeto
        if char.isalpha():
            key_char = key[i % key_length]  # Obtiene el carácter de la clave para esta posición
            shift = ord(key_char) - ord('A') if key_char.isupper() else ord(key_char) - ord('a')

            # Cifra el carácter y lo agrega al texto cifrado
            if char.isupper():
                encrypted_text += chr((ord(char) + shift - 65) % 26 + 65)
            else:
                encrypted_text += chr((ord(char) + shift - 97) % 26 + 97)
        else:
            # Si el carácter no es una letra, se agrega directamente al texto cifrado
            encrypted_text += char

    return encrypted_text  # Retorna el texto cifrado

# Función para descifrar un texto cifrado con el cifrado de Vigenère
def vigenere_decipher(text, key):
    decrypted_text = ""  # Inicializa la variable para almacenar el texto descifrado
    key_length = len(key)  # Obtiene la longitud de la clave

    # Itera a través de cada carácter del texto cifrado
    for i in range(len(text)):
        char = text[i]  # Obtiene un carácter del texto cifrado

        # Verifica si el carácter es una letra del alfabeto
        if char.isalpha():
            key_char = key[i % key_length]  # Obtiene el carácter de la clave para esta posición
            shift = ord(key_char) - ord('A') if key_char.isupper() else ord(key_char) - ord('a')

            # Descifra el carácter y lo agrega al texto descifrado
            if char.isupper():
                decrypted_text += chr((ord(char) - shift - 65) % 26 + 65)
            else:
                decrypted_text += chr((ord(char) - shift - 97) % 26 + 97)
        else:
            # Si el carácter no es una letra, se agrega directamente al texto descifrado
            decrypted_text += char

    return decrypted_text  # Retorna el texto descifrado

# Ejemplo de uso del cifrado de Vigenère
message = "Hello, this is a secret message."  # Mensaje a cifrar
key = "KEY"  # Clave para el cifrado

# Cifrar el mensaje
encrypted_message = vigenere_cipher(message, key)
print("Mensaje cifrado:", encrypted_message)

# Descifrar el mensaje
decrypted_message = vigenere_decipher(encrypted_message, key)
print("Mensaje descifrado:", decrypted_message)
