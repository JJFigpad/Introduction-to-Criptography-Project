from django import forms

class CryptoForm(forms.Form):
    OPERATION_CHOICES = [
        ('encrypt', 'Cifrar'),
        ('decrypt', 'Descifrar')
    ]

    TYPE_DES_CHOICES = [
        ('SDES', 'SDES'),
        ('DDES', 'DDES'),
        ('TDES', 'TDES')
    ]

    MODE_CHOICES = [
        ('EBC', 'EBC'),
        ('CBC', 'CBC'),
        ('OFB', 'OFB'),
        ('CFB', 'CFB')
    ]

    operation = forms.ChoiceField(choices=OPERATION_CHOICES, label="Operation")
    type_DES = forms.ChoiceField(choices=TYPE_DES_CHOICES, label="DES type")
    mode = forms.ChoiceField(choices=MODE_CHOICES, label="Operation Mode")
    text = forms.CharField(widget=forms.Textarea, label="Plain text or ciphered")
    key = forms.CharField(max_length=10, required=False, label="Key")
    IV = forms.CharField(max_length=8, required=False, label="Initialization Vector (IV)")
