from django.shortcuts import render
from django.http import HttpResponse
from .forms import EncryptionForm
from math import gcd

# Create your views here.

class Multiplicativo:
    def __init__(self,T,k):
        self.T = T
        self.k = k
    
    def __check(self):
        if gcd(self.k, 256) == 1:
            return True
        return False
    
    def __inv(self):
        if self.__check() == True:
            for i in range(1,256):
                if (self.k*i)%256==1:
                    return i
    
    def __preProcess(self):
        r = []
        temp = ''.join(self.T.split())
        for char in temp:
            r.append(ord(char))
        return r

    def __postProcess(self, L):
        r = ''
        for i in L:
            r += chr(i)
        return r
    
    def encryption(self):
        if self.__check() == False:
            return 'Clave invalida'
        cripText = self.__preProcess()
        for i in range(len(cripText)):
            cripText[i] = cripText[i]*self.k
            cripText[i] %= 256
        return self.__postProcess(cripText)
    
    def decryption(self):
        if self.__check() == False:
            return 'Clave invalida'
        clearText = self.__preProcess()
        for i in range(len(clearText)):
            clearText[i] = clearText[i]*self.__inv()
            clearText[i] %= 256
        return self.__postProcess(clearText)

def print_multiplicativo(request):
    if request.method == 'POST':
        form = EncryptionForm(request.POST)
        if form.is_valid():
            text_to_encrypt = form.cleaned_data['text_input']
            k_value = form.cleaned_data['k_value']
            action = form.cleaned_data['action']
            
            if action == 'encrypt':
                tc = Multiplicativo(text_to_encrypt, k_value)
                enc = tc.encryption()
                context = {
                    'original_text': text_to_encrypt,
                    'result_text': enc,  # Use 'result_text' instead of 'encrypted_text'
                    'action': 'Encryption',  # Update the action
                }
                
            elif action == 'decrypt':
                tc = Multiplicativo(text_to_encrypt, k_value)
                dec = tc.decryption()
                context = {
                    'original_text': text_to_encrypt,
                    'result_text': dec,  # Use 'result_text' instead of 'encrypted_text'
                    'action': 'Decryption',  # Update the action
                }
                
            context['form'] = form
            return render(request, 'multiplicativo.html', context)
    else:
        form = EncryptionForm()

    context = {'form': form}
    return render(request, 'multiplicativo.html', context)