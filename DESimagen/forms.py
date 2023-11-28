from django import forms

class ImageCryptoForm(forms.Form):
    OPERATION_CHOICES = [
        ('encrypt', 'Encrypt'),
        ('decrypt', 'Decrypt')
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
    image_input = forms.ImageField(label="Image")
    key = forms.CharField(max_length=10, required=False, label="Key")
    IV = forms.CharField(max_length=8, required=False, label="Initialization Vector (IV)")
