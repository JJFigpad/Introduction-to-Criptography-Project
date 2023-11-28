from django.shortcuts import render
from django.http import HttpResponse
from .forms import EncryptionForm
from random import choices
from sympy import Matrix, gcd
from matplotlib import pyplot as plt
import numpy as np
from io import BytesIO
import base64

# Create your views here.
class Hill_image:
  def __init__(self,I):
    self.I = I
    self.enc = None

  def __keyMatrix(self, d1):
    z256 = list(range(256))
    r = []
    while r == []:
      for i in range(d1):
        r.append(choices(z256,k = d1))
      r = Matrix(r)
      if r.det()%256 == 0 or gcd(r.det(),256) != 1:
        r = []
    return np.array(r)

  def __kMinv(self):
    return self.k.inv_mod(256)

  def encrypt(self):
    clearImage = plt.imread(self.I)
    data = np.asarray(clearImage)
    data = data.astype(int)
    mn,d1,d2 = data.shape
    key = self.__keyMatrix(d2)
    cImage = []
    for i in range(mn):
      cImage.append(np.dot(data[i],key))
    r = np.array(cImage, dtype=np.uint8)
    return r

def print_hillI(request):
    if request.method == 'POST':
        form = EncryptionForm(request.POST, request.FILES)
        if form.is_valid():
            image_to_encrypt = form.cleaned_data['image_input']
            action = form.cleaned_data['action']
            
            if action == 'encrypt':
                im = plt.imread(image_to_encrypt)
                im = np.asarray(im)
                im = np.array(im, dtype=np.uint8)
                buf_or = BytesIO()
                plt.imsave(buf_or, im, format='jpg')
                or_base64 = base64.b64encode(buf_or.getvalue()).decode('utf-8')
                tc = Hill_image(image_to_encrypt)
                enc = tc.encrypt()
                buf = BytesIO()
                plt.imsave(buf, enc, format='png')  # Specify the format and cmap
                enc_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
                context = {
                    'original_image': or_base64,
                    'result_image': enc_base64,
                    'action': 'Encryption',
                }
                
            context['form'] = form
            return render(request, 'HillI.html', context)
    else:
        form = EncryptionForm()

    context = {'form': form}
    return render(request, 'HillI.html', context)