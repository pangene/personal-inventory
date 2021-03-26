from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from .forms import SignUpForm, PasswordVerificationForm


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


@method_decorator(login_required, name='dispatch')
class DeleteConfirmView(FormView):
    """View to confirm deletion."""
    template_name = 'registration/delete_confirm.html'
    form_class = PasswordVerificationForm
    success_url = '/accounts/delete_done/'

    def get_form_kwargs(self):
        """Passes user into form for validation."""
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):  # Password verification in forms
        return redirect('delete_done')
 

class DeleteDoneView(TemplateView):
    """View after successful account deletion"""
    template_name = 'registration/delete.html'
