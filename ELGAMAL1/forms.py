from django import forms

class CryptoForm(forms.Form):
    OPERATION_CHOICES = [
        ('encrypt', 'Encrypt'),
        ('decrypt', 'Decrypt'),
    ]

    # Field for selecting the operation (encrypt or decrypt)
    operation = forms.ChoiceField(label='Operation mode', choices=OPERATION_CHOICES)

    # Field for plaintext input or ciphertext input depending on the operation
    input = forms.CharField(label='Input', widget=forms.Textarea, required=False)

    # Fields for public and private keys
    public_key = forms.CharField(label='Public Key', required=False, widget=forms.TextInput(attrs={'readonly':'readonly'}))
    private_key = forms.CharField(label='Private Key', required=False, widget=forms.TextInput(attrs={'readonly':'readonly'}))
