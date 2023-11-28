from django import forms
from .models import Image

# class ImageUploadForm(forms.ModelForm):
#     class Meta:
#         model = Image
#         fields = ['title', 'image_file']

# class EncryptionForm(forms.Form):
#     OPERATION_CHOICES = [
#         ('encrypt', 'Encriptar'),
#         ('decrypt', 'Desencriptar'),
#     ]

#     operation = forms.ChoiceField(choices=OPERATION_CHOICES, widget=forms.RadioSelect)
#     custom_key = forms.CharField(required=False, max_length=256, widget=forms.PasswordInput(attrs={'placeholder': 'Clave personalizada'}))
#     encrypted_image_key = forms.CharField(required=False, max_length=256, widget=forms.PasswordInput(attrs={'placeholder': 'Clave de imagen encriptada'}))

# forms.py
from django import forms
from .models import Image

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['title', 'image_file']

class EncryptionForm(forms.Form):
    OPERATION_CHOICES = [
        ('encrypt', 'Encriptar'),
        ('decrypt', 'Desencriptar'),
    ]

    AES_MODE_CHOICES = [
        ('ecb', 'ECB'),
        ('cbc', 'CBC'),
        ('cfb', 'CFB'),
        ('ofb', 'OFB'),
        ('ctr', 'CTR'),
    ]

    operation = forms.ChoiceField(choices=OPERATION_CHOICES, widget=forms.RadioSelect)
    aes_mode = forms.ChoiceField(choices=AES_MODE_CHOICES, widget=forms.RadioSelect)

    custom_key = forms.CharField(required=False, max_length=256, widget=forms.PasswordInput(attrs={'placeholder': 'Clave personalizada'}))
    encrypted_image_key = forms.CharField(required=False, max_length=256, widget=forms.PasswordInput(attrs={'placeholder': 'Clave de imagen encriptada'}))
    encrypted_image_iv = forms.CharField(required=False,max_length=32,widget=forms.PasswordInput(attrs={'placeholder':'Iv de la imagen'}))
