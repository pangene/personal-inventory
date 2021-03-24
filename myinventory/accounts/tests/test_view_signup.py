from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model

from ..views import signup
from ..forms import SignUpForm

User = get_user_model()

class RegistrationTests(TestCase):
    """Tests for basic registration."""

    def setUp(self):
        url = reverse('register')
        self.response = self.client.get(url)

    def test_register_status_code(self):
        """Tests the registration page is viewable."""
        self.assertEqual(self.response.status_code, 200)

    def test_register_url_resolves_signup_view(self):
        """Tests that the register url resolves to the correct view."""
        view = resolve('/accounts/register/')
        self.assertEqual(view.func, signup)

    def test_csrf(self):
        """Tests a CSRF token exists on the form."""
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        """Tests a SignUpForm exists."""
        form = self.response.context.get('form')
        self.assertIsInstance(form, SignUpForm)

    def test_form_inputs(self):
        """Verifies the amount and types of the input fields."""
        self.assertContains(self.response, '<input', 4)
        self.assertContains(self.response, 'type="email"', 1)
        self.assertContains(self.response, 'type="password"', 2)


class SuccessfulSignUpTests(TestCase):
    """Tests a new user is properly created through registration form."""

    def setUp(self):
        url = reverse('register')
        data = {
            'email': 'john@doe.com',
            'password1': 'coolguy64',
            'password2': 'coolguy64'
        }
        self.response = self.client.post(url, data)
        self.home_url = reverse('home')

    def test_redirection(self):
        """A valid form submission should redirect the user to the home page."""
        self.assertRedirects(self.response, self.home_url)

    def test_user_creation(self):
        """User should be created from valid form."""
        self.assertTrue(User.objects.exists())

    def test_user_authentication(self):
        """The redirected home url should now show the user is authenticated."""
        response = self.client.get(self.home_url)
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)


class InvalidSignUpTests(TestCase):
    """Tests invalid form inputs fail."""

    def setUp(self):
        url = reverse('register')
        self.response = self.client.post(url, {})  # submit an empty dictionary

    def test_signup_status_code(self):
        """An invalid form submission should return to the same page."""
        self.assertEqual(self.response.status_code, 200)

    def test_form_errors(self):
        """Form should have errors"""
        form = self.response.context.get('form')
        self.assertTrue(form.errors)

    def test_dont_create_user(self):
        """User not created from invalid input."""
        self.assertFalse(User.objects.exists())
