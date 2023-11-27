from django import forms

class EncryptionForm(forms.Form):
    image_input = forms.ImageField(label="Image")
    action = forms.ChoiceField(
        label="Select Action",
        choices=[("encrypt", "Encrypt"), ("decrypt", "Decrypt")],
        initial="encrypt",  # Set the default choice
        widget=forms.RadioSelect
    )
