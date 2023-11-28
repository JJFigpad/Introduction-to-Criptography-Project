from django.shortcuts import render
from django.http import HttpResponse
from .forms import ImageCryptoForm
from .image_encryption import *
from tempfile import NamedTemporaryFile
import os
import base64

def get_base64_from_image(image_path):
    with open(image_path, 'rb') as image_file:
        base64_image = base64.b64encode(image_file.read()).decode('utf-8')
    return base64_image

def crypto_view(request):
    if request.method == 'POST':
        form = ImageCryptoForm(request.POST, request.FILES)
        if form.is_valid():
            operation = form.cleaned_data['operation']
            type_DES = form.cleaned_data['type_DES']
            mode = form.cleaned_data['mode']
            image_input = form.cleaned_data['image_input']
            key = form.cleaned_data['key'] or generate_key()  
            IV = form.cleaned_data['IV'] or generate_IV()  
            # Save the uploaded image to a temporary file
            with NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(image_input.read())
                image_path = temp_file.name

            or_base64 = get_base64_from_image(image_path)
            
            with Image.open(image_path) as img:  # Open the image from the provided path
                pixel_array = np.array(img)      # Convert the image to a NumPy array
                pixel_bytes = pixel_array.tobytes()  # Convert the NumPy array to bytes
            
            img_size = img.size

            if operation == 'encrypt':
                result_bytes = encrypt_image(type_DES, mode, pixel_bytes, key, IV)
            else:
                result_bytes = decrypt_image(type_DES, mode, pixel_bytes, key, IV)

            pixel_array = np.frombuffer(result_bytes, dtype=np.uint8).reshape(img_size[1], img_size[0], -1)
            img = Image.fromarray(pixel_array)

            img.save("encriptada.png")
            enc_base64 = get_base64_from_image("encriptada.png")

            # Remove the temporary image file
            os.remove(image_path)

            context = {
                    'original_image': or_base64,
                    'result_image': enc_base64,
                    'action': operation,
                }

            context['form'] = form
            return render(request, 'DESimagen.html', context)

    else:
        form = ImageCryptoForm()

    context = {'form': form}
    return render(request, 'DESimagen.html', context)
