from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from .forms import SignUpForm


class SignUpView(FormView):
    """View for signing up."""
    template_name = 'registration/signup.html'
    form_class = SignUpForm
    success_url = '/'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


@method_decorator(login_required, name='dispatch')
class ProfileView(TemplateView):
    """View for the account profile."""
    template_name = 'profile.html'
