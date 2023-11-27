# tu_app/forms.py

from django import forms

# class RabinCryptoForm(forms.Form):
#     message = forms.CharField(label='Mensaje', widget=forms.Textarea)
#     bits = forms.IntegerField(label='Bits', initial=60)
#     action = forms.ChoiceField(
#         label='Acción',
#         choices=[('encrypt', 'Cifrar'), ('decrypt', 'Descifrar')],
#         initial='encrypt',
#         widget=forms.RadioSelect,
#     )
from django import forms

class CryptoForm(forms.Form):
    message = forms.CharField(label='Message', max_length=100)
    bits = forms.IntegerField(label='Number of bits', initial=60)
