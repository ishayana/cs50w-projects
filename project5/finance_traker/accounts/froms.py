from django import forms
from .models import User
from django.core.exceptions import ValidationError

class RegistrationForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder' : 'Username'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder' : 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder' : 'Password'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder' : 'Confirm password'}))
    
    def clean_email(self):
        email = self.cleaned_data['email']
        user =  User.objects.filter(email=email).exists()
        if user:
            raise ValidationError('This email exist already!')
        return email
    
    def clean_username(self):
        username = self.cleaned_data['username']
        user =  User.objects.filter(username=username).exists()
        if user:
            raise ValidationError('This username exist already!')
        return username
    

    def clean(self):
        cleaned_data = super().clean()
        password =  cleaned_data.get('password')
        password1  = cleaned_data.get('password1')

        if password and password1 and password != password1:
            raise ValidationError('Passwords do not match!')

class LoginForm(forms.Form):
    username = forms.CharField(label=False, widget=forms.TextInput(attrs={'placeholder' : 'Username'}))
    password = forms.CharField(label=False, widget=forms.PasswordInput(attrs={'placeholder' : 'Password'}))