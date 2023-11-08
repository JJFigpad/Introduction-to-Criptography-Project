from django import forms

class EncryptionForm(forms.Form):
    text_input = forms.CharField(label="Text")
    action = forms.ChoiceField(
        label="Select Action",
        choices=[("encrypt", "Encrypt"), ("decrypt", "Decrypt")],
        initial="encrypt",  # Set the default choice
        widget=forms.RadioSelect
    )
