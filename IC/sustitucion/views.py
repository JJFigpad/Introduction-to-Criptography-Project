from django.shortcuts import render
from django.http import HttpResponse
from .forms import EncryptionForm
from random import shuffle

# Create your views here.

class Sustitucion:
    def __init__(self, T):
        self.T = T
        self.k = list(range(256))
        shuffle(self.k)

    def __inv(self):
        temp = {}
        inv = []
        for i in range(len(self.k)):
            temp[self.k[i]] = i
        for i in range(len(self.k)):
            inv.append(temp[i])
        return inv

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
        r = []
        temp = []
        for i in range(256):
            temp.append(self.k[i])
            if i%10 == 0 and i != 0:
                r.append(', '.join(map(str, temp)))
                temp = []
        return r

    def encryption(self):
        cripText = self.__preProcess()
        for i in range(len(cripText)):
            cripText[i] = self.k[cripText[i]]
        return self.__postProcess(cripText)

    def decryption(self):
        clearText = self.__preProcess()
        inv = self.__inv()
        for i in range(len(clearText)):
            clearText[i] = inv[clearText[i]]
        return self.__postProcess(clearText)

def print_sustitucion(request):
    if request.method == 'POST':
        form = EncryptionForm(request.POST)
        if form.is_valid():
            text_to_encrypt = form.cleaned_data['text_input']
            action = form.cleaned_data['action']
            
            if action == 'encrypt':
                tc = Sustitucion(text_to_encrypt)
                enc = tc.encryption()
                key = tc.get_key()
                context = {
                    'original_text': text_to_encrypt,
                    'result_text': enc,  # Use 'result_text' instead of 'encrypted_text'
                    'action': 'Encryption',  # Update the action
                    'key':key,
                }
                
            elif action == 'decrypt':
                tc = Sustitucion(text_to_encrypt)
                dec = tc.decryption()
                context = {
                    'original_text': text_to_encrypt,
                    'result_text': dec,  # Use 'result_text' instead of 'encrypted_text'
                    'action': 'Decryption',  # Update the action
                }
                
            context['form'] = form
            return render(request, 'sustitucion.html', context)
    else:
        form = EncryptionForm()

    context = {'form': form}
    return render(request, 'sustitucion.html', context)