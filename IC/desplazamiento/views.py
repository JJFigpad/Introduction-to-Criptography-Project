from django.shortcuts import render
from django.http import HttpResponse
from .forms import EncryptionForm
import random

# Create your views here.

class Desplazamiento:
    def __init__(self, T, k):
        self.T = T
        self.k = k

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
        cripText = self.__preProcess()
        for i in range(len(cripText)):
            if isinstance(cripText[i], int):
                cripText[i] += self.k
                cripText[i] %= 256  # Adjust for the 256-character range
        return self.__postProcess(cripText)

    def decryption(self):
        clearText = self.__preProcess()
        for i in range(len(clearText)):
            if isinstance(clearText[i], int):
                clearText[i] -= self.k
                clearText[i] %= 256  # Adjust for the 256-character range
        return self.__postProcess(clearText)

def print_desplazamiento(request):
    if request.method == 'POST':
        form = EncryptionForm(request.POST)
        if form.is_valid():
            text_to_encrypt = form.cleaned_data['text_input']
            k_value = form.cleaned_data['k_value']
            action = form.cleaned_data['action']
            
            if action == 'encrypt':
                tc = Desplazamiento(text_to_encrypt, k_value)
                enc = tc.encryption()
                context = {
                    'original_text': text_to_encrypt,
                    'result_text': enc,  # Use 'result_text' instead of 'encrypted_text'
                    'action': 'Encryption',  # Update the action
                }
                
            elif action == 'decrypt':
                tc = Desplazamiento(text_to_encrypt, k_value)
                dec = tc.decryption()
                context = {
                    'original_text': text_to_encrypt,
                    'result_text': dec,  # Use 'result_text' instead of 'encrypted_text'
                    'action': 'Decryption',  # Update the action
                }
                
            context['form'] = form
            return render(request, 'desplazamiento.html', context)
    else:
        form = EncryptionForm()

    context = {'form': form}
    return render(request, 'desplazamiento.html', context)