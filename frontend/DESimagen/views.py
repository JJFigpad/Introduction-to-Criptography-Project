from django.shortcuts import render
from django.http import HttpResponse
from .forms import ImageCryptoForm
from image_encryption import *
from tempfile import NamedTemporaryFile
import os
import base64

def get_base64_from_image(image_path):
    with open(image_path, 'rb') as image_file:
        base64_image = base64.b64encode(image_file.read()).decode('utf-8')
    return base64_image

def encrypt_image_view(request):
    if request.method == 'POST':
        if request.method == 'POST':
            form = ImageCryptoForm(request.POST)
        if form.is_valid():
            operation = form.cleaned_data['operation']
            type_DES = form.cleaned_data['type_DES']
            mode = form.cleaned_data['mode']
            image_to_encrypt = form.cleaned_data['image_input']
            key = form.cleaned_data['key'] or generate_key()  
            IV = form.cleaned_data['IV'] or generate_IV()  
            # Save the uploaded image to a temporary file
            with NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(image_to_encrypt.read())
                image_path = temp_file.name
            
            or_base64 = get_base64_from_image(image_path)
            img_bytes = [i for i in base64.b64decode(or_base64)]
            img_bytes = [get_binary(i, 8) for i in img_bytes]

            if operation == 'encrypt':
                result_bytes = encrypt_image(type_DES, mode, img_bytes, key, IV)
            else:
                result_bytes = decrypt_image(type_DES, mode, img_bytes, key, IV)

            enc_base64 = base64.b64encode(result_bytes)

            # Remove the temporary image file
            os.remove(image_path)

            context = {
                    'original_image': or_base64,
                    'result_image': enc_base64,
                    'action': 'Encryption',
                }

            context['form'] = form
            return render(request, 'DESimagenes.html', context)

    else:
        form = ImageCryptoForm()

    return render(request, 'DESimagen.html', {'form': form})
