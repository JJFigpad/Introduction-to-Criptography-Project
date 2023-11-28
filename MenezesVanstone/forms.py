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

    # Private key
    private_key = forms.CharField(label='Private Key', required=False, widget=forms.TextInput(attrs={'readonly':'readonly'}))

    #Public key
    public_alpha = forms.CharField(label='Public alpha', required=False, widget=forms.TextInput(attrs={'readonly':'readonly'}))
    public_beta = forms.CharField(label='Public beta', required=False, widget=forms.TextInput(attrs={'readonly':'readonly'}))