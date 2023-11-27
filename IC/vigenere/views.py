# Importa HttpResponse y render
from django.http import HttpResponse
from django.shortcuts import render
from . import views
from .utils import vigenere_cipher, vigenere_decipher

def vigenere(request):
    if request.method == 'POST':
        text = request.POST.get('text')  # Obtiene el texto del formulario
        key = request.POST.get('key')    # Obtiene la clave del formulario

        # Verifica si el usuario eligió cifrar o descifrar (mediante un formulario o un parámetro adicional)
        if 'encrypt' in request.POST:
            result = vigenere_cipher(text, key)
            context = {'result': result, 'operation': 'Cifrado'}
        elif 'decrypt' in request.POST:
            result = vigenere_decipher(text, key)
            context = {'result': result, 'operation': 'Descifrado'}
        else:
            context = {}

        return render(request, 'vigenere_form.html', context)

    return render(request, 'vigenere_form.html')
