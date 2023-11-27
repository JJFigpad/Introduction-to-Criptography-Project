
from SDES import SDES

class DDES:
    def __init__(self, key):
        # Initialize with a single key
        self.sdes = SDES(key)

    def encrypt(self, plaintext):
        # Encrypt with SDES, then encrypt the result again with SDES
        intermediate_cipher = self.sdes.encrypt(plaintext)
        final_cipher = self.sdes.encrypt(intermediate_cipher)
        return final_cipher

    def decrypt(self, ciphertext):
        # Decrypt with SDES, then decrypt the result again with SDES
        intermediate_plain = self.sdes.decrypt(ciphertext)
        final_plain = self.sdes.decrypt(intermediate_plain)
        return final_plain
