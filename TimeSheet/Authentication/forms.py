from django import forms 
from django.contrib.auth.models import User

class loginForm(forms.ModelForm):
    class meta:
        model = User
        fields = ('username','password')
        widget = {
            'username': forms.TextInput(attrs={'class':'form-control'}),
            'password': forms.TextInput(attrs={'class':'form-control'})
        }