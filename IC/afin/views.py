from django.shortcuts import render
from django.http import HttpResponse
from .forms import EncryptionForm
from math import gcd
from random import choice
<<<<<<< HEAD
from operator import itemgetter
=======

# Create your views here.
>>>>>>> main

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
    
<<<<<<< HEAD
    def __inv(self, a):
        for i in range(256):
            if (a*i)%256 == 1:
                return i
        return 'Clave invalida'
=======
    def __inv(self):
        for i in range(256):
            if (self.k[0]*i)%256 == 1:
                return i
>>>>>>> main
            
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

<<<<<<< HEAD
    def __Ngrams(self, n):
        l = [self.T[i:i+n] for i in range (0, len(self.T)-n+1)]
        length = len(l)
        frec = {}
        for i in l:
            if i not in frec.keys():
                frec[i] = 1
            frec[i] += 1
        for i in frec.keys():
            frec[i] /= length
        frec = dict(sorted(frec.items(), key = itemgetter(1)))
        #r = abs(ord(list(frec.keys())[-1]) - ord('e'))
        return list(frec.keys())[-1],frec[list(frec.keys())[-1]]
    
    def decryption(self, a, b):
        letter1 = self.__Ngrams(1)
        letter3 = self.__Ngrams(3)
        clearText = self.__preProcess()
        for i in range(len(clearText)):
            if isinstance(clearText[i], int):
                clearText[i] = self.__inv(a)*(clearText[i]-b)
                clearText[i] %= 256  # Adjust for the 256-character range
        return self.__postProcess(clearText),letter1,letter3
=======
    def decryption(self):
        clearText = self.__preProcess()
        inv = self.__inv()
        for i in range(len(clearText)):
            clearText[i] = (inv*(clearText[i]-self.k[0]))%256
        return self.__postProcess(clearText)
>>>>>>> main

def print_afin(request):
    if request.method == 'POST':
        form = EncryptionForm(request.POST)
        if form.is_valid():
            text_to_encrypt = form.cleaned_data['text_input']
<<<<<<< HEAD
            a_value = form.cleaned_data['a_value']
            b_value = form.cleaned_data['b_value']
=======
>>>>>>> main
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
<<<<<<< HEAD
                dec,most_frequent_letter,most_frequent_trigram = tc.decryption(a_value, b_value)
                print('Most Frequent Letter:', most_frequent_letter)
                print('Most Frequent Trigram:', most_frequent_trigram)
                context = {
                    'original_text': text_to_encrypt,
                    'result_text': dec,
                    'action': 'Decryption',
                    'most_frequent_letter': most_frequent_letter,
                    'most_frequent_trigram': most_frequent_trigram,
=======
                dec = tc.decryption()
                context = {
                    'original_text': text_to_encrypt,
                    'result_text': dec,  # Use 'result_text' instead of 'encrypted_text'
                    'action': 'Decryption',  # Update the action
>>>>>>> main
                }
                
            context['form'] = form
            return render(request, 'afin.html', context)
    else:
        form = EncryptionForm()

    context = {'form': form}
    return render(request, 'afin.html', context)