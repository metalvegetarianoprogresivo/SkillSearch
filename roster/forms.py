from django import forms

class sendForm(forms.Form):
  title  = forms.CharField(label='title', max_length=100)