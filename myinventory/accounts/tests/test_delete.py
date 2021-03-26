from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

from ..views import deleteView, DeleteConfirmView


User = get_user_model()


# Note: does not test for not logged in users.
# Trusting the decorators work fine.


class DeleteSetup(TestCase):
    def setUp(self):
        # Creating new user and logging in
        email = 'test@test.com'
        self.password = 'cooltest'
        self.user = User.objects.create(email=email)
        self.user.set_password('cooltest')
        self.user.save()
        self.client.login(email=email, password=self.password)


class DeleteConfirmTests(DeleteSetup):
    """Tests the delete confirmation view."""

    def setUp(self):
        super().setUp()
        # Going to delete confirmation
        self.url = reverse('delete_confirm')
        self.response = self.client.get(self.url)

    def test_status_code(self):
        """Should be visible to logged in users."""
        self.assertEqual(self.response.status_code, 200)

    def test_delete_confirm_url_resolves(self):
        """Delete confirm url should resolve to DeleteConfirmView."""
        view = resolve('/accounts/delete_confirm/')
        self.assertEqual(view.func.view_class, DeleteConfirmView)

    def test_delete_confirm_invalid_password(self):
        """Should return to view with field errors."""
        response = self.client.post(self.url, {})
        form = response.context.get('form')
        self.assertTrue(form.errors)

    def test_delete_confirm_valid_password(self):
        """Should redirect to deletion done page if correct password."""
        response = self.client.post(self.url, {'password': self.password})
        delete_url = reverse('delete')
        self.assertRedirects(response, delete_url)


class DeleteTests(DeleteSetup):
    """Tests user can delete account (internally deactivates)."""

    def setUp(self):
        super().setUp()
        url = reverse('delete')
        self.response = self.client.get(url)

    def test_status_code(self):
        """Should be visible to logged in users."""
        self.assertEqual(self.response.status_code, 200)

    def test_delete_url_resolves(self):
        """Delete url should resolve to DeleteView."""
        view = resolve('/accounts/delete_done/')
        self.assertEqual(view.func, deleteView)

    def test_user_deactivated(self):
        """User should be deactivated upon arriving at link."""
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)

    def test_logout_after(self):
        user = self.response.context.get('user')
        self.assertIsInstance(user, AnonymousUser)
