from django.shortcuts import render
from django.http import HttpResponse
from .forms import EncryptionForm
import random

# Create your views here.

class SDES:
    #SDES with key_lenght=10 and subkey_lenght=8
    def __init__(self, T, K):
        self.text = T
        self.key = K
        self.P10 = [3,5,2,7,4,10,1,9,8,6]
        self.P8 = [6,3,7,4,8,5,10,9]
        self.P4 = [2,4,3,1]
        self.IP = [2,6,3,1,4,8,5,7]
        self.inv_IP = [4,1,3,5,7,2,8,6]
        self.S0 = [[1,0,3,2],[3,2,1,0],[0,2,1,3],[3,1,3,2]]
        self.S1 = [[0,1,2,3],[2,0,1,3],[3,0,1,0],[2,1,0,3]]

    def get_binary_representation(number):
        # Get the binary representation as a string, removing the '0b' prefix.
        binary_string = bin(number)[2:]
        # Pad the binary representation with leading zeros if needed.
        binary_string = binary_string.zfill(5)  # Assuming you want to pad to 5 bits.
        # Convert each binary character to an integer and create a list.
        return [int(bit) for bit in binary_string]

    def permute(self, input_bits, permutation):
        # Perform permutation on input_bits using the provided permutation list
        return [input_bits[i - 1] for i in permutation] 

    def left_shift(self, key_half):
        # Perform a circular left shift (LS-1)
        return key_half[1:] + key_half[:1]

    def xor(self,list_1,list_2):
        return [list_1[i]^list_2[i] for i in range(len(list_1))]
    
    def expanded_permutation(self,key_half):
        return self.permute(key_half,[4,1,2,3]) + self.permute(key_half,[2,3,4,1])
    
    def switch_bits(self, input):
        # Split the input into two halves and switch them
        left_half, right_half = input[:4], input[4:]
        return right_half + left_half
    
    def generate_subkeys(self):
        # Generate random integers from 0 to 31 to get subkeys
        k_1 = self.get_binary(random.randint(0,31))
        k_2 = self.get_binary(random.randint(0,31))
        self.subkeys = k_1,k_2
    
    def fk(self, ip_result, subkey):
        # Perform expand permutation with the subkey
        ep_result = self.expanded_permutation(subkey)
        xor_result = self.xor(subkey,ep_result)
        # Divide on two halves
        left_half,right_half = xor_result[:4], xor_result[4:]
        # Take the first and fourth bit as row and the second and third bit as a column for our S boxes
        s0_result = self.S0[2*left_half[0]+left_half[3]][2*left_half[1]+left_half[2]]
        s1_result = self.S0[2*right_half[0]+right_half[3]][2*right_half[1]+right_half[2]]
        s_result = s0_result+s1_result
        # Perform permutation P4 on S
        p4_result = self.permute(s_result,self.P4)
        # XOR the output of P4 with the left half of IP
        left_result = self.xor(p4_result,ip_result[:4])
        # Comient both halves
        return left_result+ip_result[4:]
        
    def get_subkeys(self):
        # Permute the 10-bit key using the P10 table
        p10_result = self.permute(self.key,self.P10)
        # Split the key into two halves
        left = p10_result[:5]
        right = p10_result[5:]
        # Perfom a circular left shift on each half
        left_ls = self.left_shift(left)
        right_ls = self.left_shift(right)
        # Join the two halves and permute with P8 to get the first subkey
        k_1 = self.permute(left_ls + right_ls, self.P8)
        # Perfom a double circular left shift on each half
        left_ls2 = self.left_shift(self.left_shift(left_ls))
        right_ls2 = self.left_shift(self.left_shift(right_ls))
        # Join the two halves and permute with P8 to get the second subkey
        k_2 = self.permute(left_ls2 + right_ls2, self.P8)

        self.subkeys = k_1,k_2

        return k_1,k_2
    
    def encrypt(self):
        # Perform Initial permutation on plain text
        ip_result = self.permute(self.text,self.IP)
        # Perform f_k function with the first subkey
        fk1_result = self.fk(ip_result, self.subkeys[0])
        # Perform Switch Bites function
        sw_result = self.switch_bits(fk1_result)
        # Perform f_k function with the second subkey
        fk2_result = self.fk(sw_result, self.subkeys[1])
        # Perform inverse permutation to get the ciphered text
        ciphered = self.permute(fk2_result,self.inv_IP)
        return ciphered
    
    def decrypt(self,ciphered_text):
        self.get_subkeys()
        # Perform Initial permutation on the ciphered text
        ip_result = self.permute(ciphered_text,self.IP)
        # Perform f_k function with the second subkey
        fk2_result = self.fk(ip_result, self.subkeys[1])
        # Perform Switch Bites function
        sw_result = self.switch_bits(fk2_result)
        # Perform f_k function with the first subkey
        fk1_result = self.fk(sw_result, self.subkeys[0])
        # Perform inverse permutation to get the ciphered text
        decrypted = self.permute(fk1_result,self.inv_IP)
        return decrypted

def print_sdes(request):
    if request.method == 'POST':
        form = EncryptionForm(request.POST)
        if form.is_valid():
            text_to_encrypt = form.cleaned_data['text_input']
            k_value = form.cleaned_data['k_value']
            action = form.cleaned_data['action']
            
            if action == 'encrypt':
                tc = SDES(text_to_encrypt, k_value)
                enc = tc.encrypt()
                context = {
                    'original_text': text_to_encrypt,
                    'result_text': enc,  # Use 'result_text' instead of 'encrypted_text'
                    'action': 'Encryption',  # Update the action
                }
                
            elif action == 'decrypt':
                tc = SDES(text_to_encrypt, k_value)
                dec = tc.decrypt()
                context = {
                    'original_text': text_to_encrypt,
                    'result_text': dec,  # Use 'result_text' instead of 'encrypted_text'
                    'action': 'Decryption',  # Update the action
                }
                
            context['form'] = form
            return render(request, 'SDES.html', context)
    else:
        form = EncryptionForm()

    context = {'form': form}
    return render(request, 'SDES.html', context)