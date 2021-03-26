from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model, views
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.core import mail
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes


User = get_user_model()

class PasswordResetTests(TestCase):
    """Basic tests for the password reset view."""

    def setUp(self):
        url = reverse('password_reset')
        self.response = self.client.get(url)

    def test_status_code(self):
        """Tests password reset page is viewable."""
        self.assertEqual(self.response.status_code, 200)

    def test_view_function(self):
        """Tests password reset view directs properly."""
        view = resolve('/accounts/password_reset/')
        self.assertEqual(view.func.view_class, views.PasswordResetView)

    def test_csrf(self):
        """Tests password reset form contains CSRF."""
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        """Tests password reset contains correct form."""
        form = self.response.context.get('form')
        self.assertIsInstance(form, PasswordResetForm)

    def test_form_inputs(self):
        """The view must contain two inputs: csrf and email."""
        self.assertContains(self.response, '<input', 2)
        self.assertContains(self.response, 'type="email"', 1)


class SuccessfulPasswordResetTests(TestCase):
    """Tests password reset proceeds properly after a successful form input."""

    def setUp(self):
        email = 'test@test.com'
        User.objects.create_user(email=email, password='123abcdef')
        url = reverse('password_reset')
        self.response = self.client.post(url, {'email': email})

    def test_redirection(self):
        """
        A valid form submission should redirect the 
        user to 'password_reset_done' view.
        """
        url = reverse('password_reset_done')
        self.assertRedirects(self.response, url)

    def test_send_password_reset_email(self):
        """A valid form submission should send an email."""
        self.assertEqual(1, len(mail.outbox))


class InvalidPasswordResetTests(TestCase):
    """Tests invalid password reset form submissions fail."""

    def setUp(self):
        url = reverse('password_reset')
        self.response = self.client.post(url, {'email': 'donotexist@email.com'})

    def test_redirection(self):
        """
        Even invalid emails in the database should 
        redirect the user to 'password_reset_done' view.
        """
        url = reverse('password_reset_done')
        self.assertRedirects(self.response, url)

    def test_no_reset_email_sent(self):
        """Invalid emails not in database should not be sent an email."""
        self.assertEqual(0, len(mail.outbox))


class PasswordResetDoneTests(TestCase):
    """Tests the password reset done view."""

    def setUp(self):
        url = reverse('password_reset_done')
        self.response = self.client.get(url)

    def test_status_code(self):
        """Assures password reset done page is viewable."""
        self.assertEqual(self.response.status_code, 200)

    def test_view_function(self):
        """Assures reset done directs to the right page."""
        view = resolve('/accounts/password_reset/done/')
        self.assertEqual(view.func.view_class, views.PasswordResetDoneView)


class PasswordResetConfirmTests(TestCase):
    """Tests the password reset confirm view."""

    def setUp(self):
        user = User.objects.create_user(email='john@doe.com', password='123abcdef')

        # Create a valid password reset token
        # based on how django creates the token internally:
        # https://github.com/django/django/blob/1.11.5/django/contrib/auth/forms.py#L280
        self.uid = urlsafe_base64_encode(force_bytes(user.pk))
        self.token = default_token_generator.make_token(user)

        url = reverse('password_reset_confirm', kwargs={'uidb64': self.uid, 'token': self.token})
        self.response = self.client.get(url, follow=True)

    def test_status_code(self):
        """Assures password reset confirm page is viewable."""
        self.assertEqual(self.response.status_code, 200)

    def test_view_function(self):
        """Assures reset confirm directs to the right page."""
        view = resolve(f'/accounts/reset/{self.uid}/{self.token}/')
        self.assertEqual(view.func.view_class, views.PasswordResetConfirmView)

    def test_csrf(self):
        """Tests password reset confirm form contains CSRF."""
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        """Tests password reset confirm view contains the correct form."""
        form = self.response.context.get('form')
        self.assertIsInstance(form, SetPasswordForm)

    def test_form_inputs(self):
        """The view must contain two inputs: csrf and two password fields."""
        self.assertContains(self.response, '<input', 3)
        self.assertContains(self.response, 'type="password"', 2)


class InvalidPasswordResetConfirmTests(TestCase):
    """Tests password reset confirm invalides correctly."""

    def setUp(self):
        user = User.objects.create_user(email='john@doe.com', password='123abcdef')
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        # invalidate the token by changing the password
        user.set_password('abcdef123')
        user.save()

        url = reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
        self.response = self.client.get(url)

    def test_status_code(self):
        """Test view status is correct."""
        self.assertEqual(self.response.status_code, 200)

    def test_html(self):
        """Test the view displays the reset was invalid."""
        password_reset_url = reverse('password_reset')
        self.assertContains(self.response, 'password reset link was invalid')
        self.assertContains(self.response, f'href="{password_reset_url}"')


class PasswordResetCompleteTests(TestCase):
    """Tests the password reset complete view."""

    def setUp(self):
        url = reverse('password_reset_complete')
        self.response = self.client.get(url)

    def test_status_code(self):
        """Tests status code is correct."""
        self.assertEqual(self.response.status_code, 200)

    def test_view_function(self):
        """Tests view directs properly."""
        view = resolve('/accounts/reset/done/')
        self.assertEqual(view.func.view_class, views.PasswordResetCompleteView)


class PasswordResetMailTests(TestCase):
    """Tests the password reset email is correct."""

    def setUp(self):
        User.objects.create_user(email='john@doe.com', password='123')
        self.response = self.client.post(reverse('password_reset'), { 'email': 'john@doe.com' })
        self.email = mail.outbox[0]

    def test_email_subject(self):
        """Test the password reset email subject is correct."""
        self.assertEqual('[Do I own?] Password Reset', self.email.subject)

    def test_email_body(self):
        """Test the password reset body is correct."""
        context = self.response.context
        token = context.get('token')
        uid = context.get('uid')
        password_reset_token_url = reverse('password_reset_confirm', kwargs={
            'uidb64': uid,
            'token': token
        })
        self.assertIn(password_reset_token_url, self.email.body)
        self.assertIn('john', self.email.body)
        self.assertIn('john@doe.com', self.email.body)

    def test_email_to(self):
        """Test the email is sent to the correct email."""
        self.assertEqual(['john@doe.com',], self.email.to)
