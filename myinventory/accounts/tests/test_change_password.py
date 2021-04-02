from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model, views
from django.contrib.auth.forms import PasswordChangeForm

User = get_user_model()

class PasswordChangeSetup(TestCase):
    """Set up for the below Password Change tests."""

    def setUp(self):
        # Creating new user and logging in
        # No need to test login decorator!
        email = 'test@test.com'
        self.password = 'cooltest'
        self.user = User.objects.create(email=email)
        self.user.set_password('cooltest')
        self.user.save()
        self.client.login(email=email, password=self.password)
        # Going to password change
        self.url = reverse('password_change')
        self.response = self.client.get(self.url)


class PasswordChangeTests(PasswordChangeSetup):
    """Basic tests for PasswordChange."""

    def test_status_code(self):
        """Tests password change page is viewable."""
        self.assertEqual(self.response.status_code, 200)

    def test_view_function(self):
        """Tests password change view directs properly."""
        view = resolve('/accounts/password_change/')
        self.assertEqual(view.func.view_class, views.PasswordChangeView)

    def test_csrf(self):
        """Tests password change form contains CSRF."""
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        """Tests password change contains correct form."""
        form = self.response.context.get('form')
        self.assertIsInstance(form, PasswordChangeForm)

    def test_form_inputs(self):
        """The view must contain: csrf, 3 passwords, a submit."""
        self.assertContains(self.response, '<input', 4)
        self.assertContains(self.response, 'type="password"', 3)
        self.assertContains(self.response, '<button', 2)  # submit + nav


class PasswordChangeSuccessTests(PasswordChangeSetup):
    """Tests successfully changing password."""

    def setUp(self):
        super().setUp()
        self.new_password = 'testcool'
        data = {
            'old_password': self.password,
            'new_password1': self.new_password,
            'new_password2': self.new_password
        }
        self.response = self.client.post(self.url, data)

    def test_redirection(self):
        """
        A valid form submission should redirect the 
        user to 'password_change_done' view.
        """
        url = reverse('password_change_done')
        self.assertRedirects(self.response, url)

    def test_password_changes(self):
        """Password should change after valid form submission."""
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(self.new_password))


class PasswordChangeInvalidTests(PasswordChangeSetup):
    """Tests invalid form submissions to password change."""

    def setUp(self):
        super().setUp()
        data = {
            'old_password': 'no',
            'new_password1': 'woah',
            'new_password2': 'joe'
        }
        self.response = self.client.post(self.url, data)

    def test_same_page(self):
        """Should remain on the same url."""
        view = resolve('/accounts/password_change/')
        self.assertEqual(view.func.view_class, views.PasswordChangeView)

    def test_password_no_changes(self):
        """Password should not change after invalid submission."""
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(self.password))
        