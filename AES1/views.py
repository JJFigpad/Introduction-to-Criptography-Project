# views.py
from django.shortcuts import render, redirect
from .models import Image
from .forms import ImageUploadForm, EncryptionForm
from .utils import generate_aes_key_and_iv

def image_upload(request):
    if request.method == 'POST':
        image_form = ImageUploadForm(request.POST, request.FILES)
        encryption_form = EncryptionForm(request.POST)

        if image_form.is_valid() and encryption_form.is_valid():
            image_instance = image_form.save()

            operation = encryption_form.cleaned_data['operation']
            custom_key = encryption_form.cleaned_data['custom_key']
            custom_iv = encryption_form.cleaned_data['custom_iv']
            encrypted_image_key = encryption_form.cleaned_data['encrypted_image_key']
            encrypted_image_iv = encryption_form.cleaned_data['encrypted_image_iv']

            if operation == 'encrypt':
                key = custom_key or generate_aes_key_and_iv()[0]
                iv =  custom_iv or generate_aes_key_and_iv()[1]
                image_instance.encrypt_image(custom_key=key,custom_iv=iv)
                

            elif operation == 'decrypt':
                # Asegúrate de obtener la clave correcta para la imagen encriptada
                key = encrypted_image_key or image_instance.encryption_key
                iv = encrypted_image_iv
                image_instance.decrypt_image(custom_key=key,encrypted_image_iv =iv)

            return redirect('image_list')
    else:
        image_form = ImageUploadForm()
        encryption_form = EncryptionForm()

    return render(request, 'AES1/image_upload.html', {'image_form': image_form, 'encryption_form': encryption_form})

def image_list(request):
    # Obtén la última instancia de Image desde la base de datos
    latest_image_instance = Image.objects.last()

    # Verifica si la última instancia es válida
    if latest_image_instance:
        # Accede a los campos que contienen las imágenes
        original_image = latest_image_instance.image_file
        encrypted_image = latest_image_instance.encrypted_image
        decrypted_image = latest_image_instance.decrypted_image

        # Agrega mensajes de impresión para depurar
        print(f"Encryption Key: {latest_image_instance.encryption_key}")
        print(f"Decryption Key: {latest_image_instance.decryption_key}")  # Asegúrate de tener esto en tu modelo
        print(f"Is Encrypted: {latest_image_instance.is_encrypted}")

        return render(request, 'AES1/image_list.html', {
            'original_image': original_image,
            'encrypted_image': encrypted_image,
            'decrypted_image': decrypted_image,
            'encryption_key': latest_image_instance.encryption_key,
            'decryption_key': latest_image_instance.decryption_key,
            'encryption_iv': latest_image_instance.encryption_iv,

            
        })
    else:
        # Si no hay ninguna instancia, pasa None para ambas imágenes
        return render(request, 'AES1/image_list.html', {
            'original_image': None,
            'encrypted_image': None,
            'decrypted_image': None,
            'encryption_key': None,
            'decryption_key': None,
        })
