class SDES:
    def __init__(self, K):
        # Initialize the SDES with a given key K (10 bits).
        # Convert the key to its binary representation.
        self.key = K
        # Permutation tables and S-Boxes for the SDES algorithm.
        self.P10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
        self.P8 = [6, 3, 7, 4, 8, 5, 10, 9]
        self.P4 = [2, 4, 3, 1]
        self.IP = [2, 6, 3, 1, 4, 8, 5, 7]
        self.inv_IP = [4, 1, 3, 5, 7, 2, 8, 6]
        self.S0 = [[1, 0, 3, 2], [3, 2, 1, 0], [0, 2, 1, 3], [3, 1, 3, 2]]
        self.S1 = [[0, 1, 2, 3], [2, 0, 1, 3], [3, 0, 1, 0], [2, 1, 0, 3]]
        # Generate the subkeys to be used in the encryption/decryption process.
        self.get_subkeys()

    def get_binary(self, number, length):
        # Convert a number to its binary representation, padded to a specified length.
        binary_string = bin(number)[2:]
        binary_string = binary_string.zfill(length)
        return binary_string

    def permute(self, input_bits, permutation):
        # Perform a permutation on input bits based on a given permutation table.
        return "".join([input_bits[i - 1] for i in permutation])

    def left_shift(self, key_half):
        # Perform a circular left shift (rotate left) on a bit string.
        return key_half[1:] + key_half[:1]

    def xor(self, str_1, str_2):
        # Perform bitwise XOR on two bit strings and return the result.
        return self.get_binary(int(str_1, 2) ^ int(str_2, 2), len(str_1))

    def expanded_permutation(self, key_half):
        # Expand and permute a 4-bit key half to 8 bits using a fixed table.
        return self.permute(key_half, [4, 1, 2, 3, 2, 3, 4, 1])

    def switch_bits(self, input):
        # Switch (swap) the left and right halves of the input bit string.
        left_half, right_half = input[:4], input[4:]
        return right_half + left_half

    def fk(self, ip_result, subkey):
        # The 'f' function in SDES, which performs operations on a subkey and part of the input.
        left_half, right_half = ip_result[:4], ip_result[4:]
        ep_result = self.expanded_permutation(right_half)
        xor_result = self.xor(ep_result, subkey)
        left_xor, right_xor = xor_result[:4], xor_result[4:]
        row_s0 = 2 * int(left_xor[0]) + int(left_xor[3])
        col_s0 = 2 * int(left_xor[1]) + int(left_xor[2])
        s0_result = self.S0[row_s0][col_s0]
        row_s1 = 2 * int(right_xor[0]) + int(right_xor[3])
        col_s1 = 2 * int(right_xor[1]) + int(right_xor[2])
        s1_result = self.S1[row_s1][col_s1]
        s_result = self.get_binary(s0_result, 2) + self.get_binary(s1_result, 2)
        p4_result = self.permute(s_result, self.P4)
        left_result = self.xor(p4_result, left_half)
        return left_result + right_half

    def get_subkeys(self):
        # Generate two subkeys from the original key for use in the encryption and decryption processes.
        p10_result = self.permute(self.key, self.P10)
        left, right = p10_result[:5], p10_result[5:]
        left_ls = self.left_shift(left)
        right_ls = self.left_shift(right)
        k_1 = self.permute(left_ls + right_ls, self.P8)
        left_ls2 = self.left_shift(self.left_shift(left_ls))
        right_ls2 = self.left_shift(self.left_shift(right_ls))
        k_2 = self.permute(left_ls2 + right_ls2, self.P8)
        self.subkeys = [k_1, k_2]

    def encrypt(self, plain_text):
        # Encrypt a plaintext using SDES. 
        # The process involves initial permutation, two rounds of fk function, switching bits, and final permutation.
        ip_result = self.permute(plain_text, self.IP)
        fk1_result = self.fk(ip_result, self.subkeys[0])
        sw_result = self.switch_bits(fk1_result)
        fk2_result = self.fk(sw_result, self.subkeys[1])
        ciphered = self.permute(fk2_result, self.inv_IP)
        return ciphered

    def decrypt(self, ciphered_text):
        # Decrypt a ciphertext using SDES.
        # The process is similar to encryption but uses the subkeys in reverse order.
        self.get_subkeys()
        ip_result = self.permute(ciphered_text, self.IP)
        fk2_result = self.fk(ip_result, self.subkeys[1])
        sw_result = self.switch_bits(fk2_result)
        fk1_result = self.fk(sw_result, self.subkeys[0])
        decrypted = self.permute(fk1_result, self.inv_IP)
        return decrypted
