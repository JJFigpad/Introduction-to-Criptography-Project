from django.shortcuts import render
from django.http import HttpResponse
from .forms import EncryptionForm
from operator import itemgetter
from random import shuffle
from operator import itemgetter

# Create your views here.
class Permutacion:
    def __init__(self, T, n):
        self.__temp = T
        self.n = n
        self.T = self.__newT()
        self.k = self.__k()

    def __newT(self):
        new = ''.join(self.__temp.split())
        new = [new[i:i+self.n] for i in range (0, len(new),self.n)]
        return new

    def __k(self):
        temp = []
        for i in self.T:
            l = len(i)
            lt = list(range(l))
            shuffle(lt)
            temp.append(lt)
        return temp

    def get_key(self):
        return self.k

    def encryption(self):
        encText = []
        for i in range(len(self.T)):
          temp = []
          for j in range(len(self.T[i])):
            temp.append(self.T[i][self.k[i][j]])
          encText.append(temp)
        shuffle(encText)
        r = ''
        for i in encText:
          for j in i:
            r += j
        return r

def print_permutacion(request):
    if request.method == 'POST':
        form = EncryptionForm(request.POST)
        if form.is_valid():
            text_to_encrypt = form.cleaned_data['text_input']
            n_value = form.cleaned_data['n_value']
            action = form.cleaned_data['action']
            
            if action == 'encrypt':
                tc = Permutacion(text_to_encrypt, n_value)
                enc = tc.encryption()
                context = {
                    'original_text': text_to_encrypt,
                    'result_text': enc,  # Use 'result_text' instead of 'encrypted_text'
                    'action': 'Encryption',  # Update the action
                }
                
            context['form'] = form
            return render(request, 'permutacion.html', context)
    else:
        form = EncryptionForm()

    context = {'form': form}
    return render(request, 'permutacion.html', context)