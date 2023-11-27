from SDES import SDES


class TDES:
    def __init__(self, key):
        # Initialize with a single key
        self.sdes = SDES(key)

    def encrypt(self, plaintext):
        # First encryption
        intermediate_cipher1 = self.sdes.encrypt(plaintext)
        # Decrypt using the same key
        intermediate_plain = self.sdes.decrypt(intermediate_cipher1)
        # Second encryption
        final_cipher = self.sdes.encrypt(intermediate_plain)
        return final_cipher

    def decrypt(self, ciphertext):
        # First decryption
        intermediate_plain1 = self.sdes.decrypt(ciphertext)
        # Encrypt using the same key
        intermediate_cipher = self.sdes.encrypt(intermediate_plain1)
        # Second decryption
        final_plain = self.sdes.decrypt(intermediate_cipher)
        return final_plain
