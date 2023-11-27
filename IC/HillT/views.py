from django.shortcuts import render
from django.http import HttpResponse
from .forms import EncryptionForm
from random import choices
from sympy import Matrix, gcd, Transpose

# Create your views here.

class Hill_text:
  def __init__(self,T):
    self.T = T.replace(' ','')
    self.m = len(self.T)
    self.k = self.__keyMatrix()

  def __preProcess(self):
    r = []
    temp = ''.join(self.T.split())
    for char in temp:
        r.append(ord(char))
    return Transpose(Matrix(r))

  def __postProcess(self, L):
    r = ''
    for i in L:
        r += chr(i)
    return r

  def __keyMatrix(self):
    z256 = list(range(256))
    r = []
    while r == []:
      for i in range(self.m):
        r.append(choices(z256,k = self.m))
      r = Matrix(r)
      if r.det()%256 == 0 or gcd(r.det(),256) != 1:
        r = []
    return r
  
  def __kMinv(self):
    return self.k.inv_mod(256)

  def encryption(self):
    clearText = self.__preProcess()
    temp = clearText*self.k
    r = []
    for i in temp:
      r.append(i%256)
    return self.__postProcess(r)

def print_hillT(request):
    if request.method == 'POST':
        form = EncryptionForm(request.POST)
        if form.is_valid():
            text_to_encrypt = form.cleaned_data['text_input']
            action = form.cleaned_data['action']
            
            if action == 'encrypt':
                tc = Hill_text(text_to_encrypt)
                enc = tc.encryption()
                key = tc.k
                context = {
                    'original_text': text_to_encrypt,
                    'result_text': enc,  # Use 'result_text' instead of 'encrypted_text'
                    'action': 'Encryption',  # Update the action
                    'key': key,
                }
                
            context['form'] = form
            return render(request, 'HillT.html', context)
    else:
        form = EncryptionForm()

    context = {'form': form}
    return render(request, 'HillT.html', context)