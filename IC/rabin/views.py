# En tu archivo views.py
from django.shortcuts import render
from .utils import perform_crypto, perform_decryption

def index(request):
    return render(request, 'rabin/index.html')

def encrypt(request):
    if request.method == 'POST':
        message = request.POST.get('message', '')
        bits = int(request.POST.get('bits', 60))
        # Lógica para cifrar el mensaje y mostrar el resultado
        result = perform_crypto(message, bits)
        return render(request, 'rabin/result.html', {'result': result, 'action': 'Encrypt'})
    return render(request, 'rabin/encrypt.html')

def decrypt(request):
    if request.method == 'POST':
        ciphertext = int(request.POST.get('ciphertext', ''))
        p = int(request.POST.get('p', ''))
        q = int(request.POST.get('q', ''))
        # Lógica para descifrar el mensaje y mostrar el resultado
        result = perform_decryption(ciphertext, p, q)
        return render(request, 'rabin/result.html', {'result': result, 'action': 'Decrypt'})
    return render(request, 'rabin/decrypt.html')