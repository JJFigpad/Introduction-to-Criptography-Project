from django.shortcuts import render
from django.http import HttpResponse
from .forms import EncryptionForm
from random import choice
from math import gcd

# Create your views here.

class RSA:
  def __init__(self,T, p = 577, q = 149, a = None, n = 3):
    self.T = T
    self.__p = p
    self.__q = q
    self.n = p*q
    self.a = a
    self.__b = None
    self.block_len = n

  def __preProcess(self):
    alf_l = []
    r = []
    temp = ''.join(self.T.split())
    for char in temp:
        alf_l.append(ord(char))
    s = 0
    for i in range(len(alf_l)):
      if i%self.block_len == 0 and i != 0:
        r.append(s)
        s = 0
      s += alf_l[i]*(256**(i%self.block_len))
    r.append(s)
    return r

  def __find(self):
    euler = (self.__p-1)*(self.__q-1)
    self.a = choice(list(range(euler)))
    while gcd(self.a, euler) > 1:
      self.a = choice(list(range(euler)))
    for i in range(euler):
      if (self.a*i)%(euler) == 1:
        self.__b = i
        break

  def bm(self, n):
    binary = bin(self.a)[2:]
    r = 1
    for i in binary:
      if i == '1':
        r = ((r**2)*n)%self.n
      else:
        r = (r**2)%self.n
    return r%self.n

  def inv_bm(self, n):
    binary = bin(self.__b)[2:]
    r = 1
    for i in binary:
      if i == '1':
        r = ((r*r)*n)%self.n
      else:
        r = (r*r)%self.n
    return r%self.n

  def encrypt(self):
    if self.a == None:
      self.__find()
    clearText = self.__preProcess()
    encText = []
    for i in clearText:
      encText.append(self.bm(i))
    return encText

  def decrypt(self):
    if self.a == None:
      self.__find()
    clearText = self.__preProcess()
    encText = []
    for i in clearText:
      encText.append(self.inv_bm(i))
    return encText

def print_rsa(request):
    if request.method == 'POST':
        form = EncryptionForm(request.POST)
        if form.is_valid():
            text_to_encrypt = form.cleaned_data['text_input']
            action = form.cleaned_data['action']
            
            if action == 'encrypt':
                tc = RSA(text_to_encrypt) #, k_value)
                enc = tc.encrypt()
                key = (tc.n, tc.a)
                context = {
                    'original_text': text_to_encrypt,
                    'result_text': enc,  # Use 'result_text' instead of 'encrypted_text',
                    'key': key,
                    'action': 'Encryption',  # Update the action
                }
                
            elif action == 'decrypt':
                tc = RSA(text_to_encrypt)
                dec = tc.decrypt()
                key = (tc.n, tc.a)
                context = {
                    'original_text': text_to_encrypt,
                    'result_text': dec,
                    'key': key,
                    'action': 'Decryption',
                }
                
            context['form'] = form
            return render(request, 'RSA.html', context)
    else:
        form = EncryptionForm()

    context = {'form': form}
    return render(request, 'RSA.html', context)