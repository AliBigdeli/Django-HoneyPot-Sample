from django import forms
from .models import LoginAttempt


class LoginForm(forms.ModelForm):
    username = forms.EmailField(required=True)
    password = forms.CharField(required=True)
    class Meta:
        model = LoginAttempt
        fields = ["username", "password"]
        