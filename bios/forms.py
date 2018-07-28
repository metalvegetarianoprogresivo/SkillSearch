from django import forms

class GetDocumentsForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput)
    password = forms.CharField(min_length=1, max_length=255, widget=forms.PasswordInput)
