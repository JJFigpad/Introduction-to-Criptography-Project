from django.shortcuts import render
from django.http import HttpResponse
from .forms import EncryptionForm
from math import gcd
from random import choice

# Create your views here.

class Afin:
    def __init__(self, T):
        self.T = T
        self.k = list(self.__k())

    def __k(self):
        coprimos = []
        for i in range(256):
            if gcd(i,256) == 1:
                coprimos.append(i)
        return choice(coprimos), choice(list(range(256)))
    
    def __inv(self):
        for i in range(256):
            if (self.k[0]*i)%256 == 1:
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
    
    def get_key(self):
        return self.k

    def encryption(self):
        cripText = self.__preProcess()
        for i in range(len(cripText)):
            cripText[i] = (self.k[0]*cripText[i]+self.k[1])%256
        return self.__postProcess(cripText)

    def decryption(self):
        clearText = self.__preProcess()
        inv = self.__inv()
        for i in range(len(clearText)):
            clearText[i] = (inv*(clearText[i]-self.k[0]))%256
        return self.__postProcess(clearText)

def print_afin(request):
    if request.method == 'POST':
        form = EncryptionForm(request.POST)
        if form.is_valid():
            text_to_encrypt = form.cleaned_data['text_input']
            action = form.cleaned_data['action']
            
            if action == 'encrypt':
                tc = Afin(text_to_encrypt)
                enc = tc.encryption()
                key = tc.get_key()
                context = {
                    'original_text': text_to_encrypt,
                    'result_text': enc,  # Use 'result_text' instead of 'encrypted_text'
                    'action': 'Encryption',  # Update the action
                    'key':key,
                }
                
            elif action == 'decrypt':
                tc = Afin(text_to_encrypt)
                dec = tc.decryption()
                context = {
                    'original_text': text_to_encrypt,
                    'result_text': dec,  # Use 'result_text' instead of 'encrypted_text'
                    'action': 'Decryption',  # Update the action
                }
                
            context['form'] = form
            return render(request, 'afin.html', context)
    else:
        form = EncryptionForm()

    context = {'form': form}
    return render(request, 'afin.html', context)