from django import forms

class EncryptionForm(forms.Form):
    text_input = forms.CharField(label="Text")
    k_value = forms.IntegerField(
        label="Value of 'k'",
        min_value=1,
        max_value=255
    )
    action = forms.ChoiceField(
        label="Select Action",
        choices=[("encrypt", "Encrypt"), ("decrypt", "Decrypt")],
        initial="encrypt",  # Set the default choice
        widget=forms.RadioSelect
    )
