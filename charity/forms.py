from django import forms
from django.contrib.auth.models import User
from django.core.validators import EmailValidator


class RegisterUserForm(forms.Form):
    name = forms.CharField(max_length=100)
    surname = forms.CharField(max_length=100)
    email = forms.CharField(max_length=100, validators=[EmailValidator(message="wrong email")])
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)


class LoginForm(forms.Form):
    email = forms.CharField(max_length=100, validators=[EmailValidator(message="wrong email")])
    password = forms.CharField(widget=forms.PasswordInput)

