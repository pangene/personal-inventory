from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django import forms

from .models import EmailUser


class SignUpForm(UserCreationForm):
    class Meta:
        model = EmailUser
        fields = ('email', 'password1', 'password2')


class PasswordVerificationForm(forms.Form):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(PasswordVerificationForm, self).__init__(*args, **kwargs)

    def clean_password(self):
        verify_password = self.cleaned_data['password']
        email = self.user.email
        user = authenticate(email=email, password=verify_password)
        if user is not None:
            return self.cleaned_data
        else:
            self.add_error('password', 'Incorrect password')
            return self.cleaned_data

