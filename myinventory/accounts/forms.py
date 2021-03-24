from django.contrib.auth.forms import UserCreationForm

from .models import EmailUser


class SignUpForm(UserCreationForm):
    class Meta:
        model = EmailUser
        fields = ('email', 'password1', 'password2')
