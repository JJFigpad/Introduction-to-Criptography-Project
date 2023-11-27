from django import forms

class EncryptionForm(forms.Form):
    text_input = forms.CharField(label="Text")
<<<<<<< HEAD
    a_value = forms.IntegerField(
        label="Value of 'a'",
        min_value=1,
        max_value=255
    )
    b_value = forms.IntegerField(
        label="Value of 'b'",
        min_value=0,
        max_value=255
    )
=======
>>>>>>> main
    action = forms.ChoiceField(
        label="Select Action",
        choices=[("encrypt", "Encrypt"), ("decrypt", "Decrypt")],
        initial="encrypt",  # Set the default choice
        widget=forms.RadioSelect
    )
