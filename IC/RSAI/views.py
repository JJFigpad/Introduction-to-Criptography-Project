from django.shortcuts import render
from django.http import HttpResponse
from .forms import EncryptionForm
from random import choice
import numpy as np
import cv2
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from tempfile import NamedTemporaryFile
import os

# Create your views here.

class RSAI:
  def __init__(self, I, p = 577, q = 149, a = None, b = None):
    self.I = I
    self.__p = p
    self.__q = q
    self.n = p*q
    self.a = a
    self.__b = b

  def __find(self):
    euler = (self.__p-1)*(self.__q-1)
    self.a = choice(list(range(euler)))
    while np.gcd(self.a, euler) > 1:
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
    if self.a is None:
      self.__find()
        
    clearImage = cv2.imread(self.I)  # Load the image array
    row, col = clearImage.shape[0], clearImage.shape[1]
    enc = np.zeros((row, col, 3), dtype=np.uint8)  # Initialize the array

    for i in range(row):
      for j in range(col):
        r, g, b = clearImage[i, j]
        C1 = self.bm(r)
        C2 = self.bm(g)
        C3 = self.bm(b)
        enc[i, j] = [C1, C2, C3]

    # Save the encrypted image array
    encrypted_path = 'path_to_save_encrypted_image.png'  # Provide the desired path
    cv2.imwrite(encrypted_path, enc)
    return encrypted_path

def get_base64_from_image(image_path):
    with open(image_path, 'rb') as image_file:
        base64_image = base64.b64encode(image_file.read()).decode('utf-8')
    return base64_image


def print_rsaI(request):
    if request.method == 'POST':
        form = EncryptionForm(request.POST, request.FILES)
        if form.is_valid():
            image_to_encrypt = form.cleaned_data['image_input']
            action = form.cleaned_data['action']

            if action == 'encrypt':
                # Save the uploaded image to a temporary file
                with NamedTemporaryFile(delete=False) as temp_file:
                    temp_file.write(image_to_encrypt.read())
                    image_path = temp_file.name

                or_base64 = get_base64_from_image(image_path)

                tc = RSAI(image_path)
                enc_path = tc.encrypt()
                enc_base64 = get_base64_from_image(enc_path)

                # Remove the temporary image file
                os.remove(image_path)

                context = {
                    'original_image': or_base64,
                    'result_image': enc_base64,
                    'action': 'Encryption',
                }

            context['form'] = form
            return render(request, 'RSAI.html', context)
    else:
        form = EncryptionForm()

    context = {'form': form}
    return render(request, 'RSAI.html', context)