from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

from ..views import DeleteDoneView, DeleteConfirmView

User = get_user_model()


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
    """Tests the DeleteConfirmView, which actually deletes user."""

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
        """
        Should delete user and redirect to deletion 
        done page if correct password.
        """
        response = self.client.post(self.url, {'password': self.password})
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)
        delete_url = reverse('delete_done')
        self.assertRedirects(response, delete_url)


class DeleteDoneTests(DeleteSetup):
    """Tests the DeleteDoneView, after deletion."""

    def setUp(self):
        super().setUp()
        # First posts a successful password.
        confirm_url = reverse('delete_confirm')
        self.client.post(confirm_url, {'password': self.password})
        # Then redirects to done page.
        url = reverse('delete_done')
        self.response = self.client.get(url)

    def test_status_code(self):
        """Should be visible to logged in users."""
        self.assertEqual(self.response.status_code, 200)

    def test_delete_url_resolves(self):
        """Delete url should resolve to DeleteView."""
        view = resolve('/accounts/delete_done/')
        self.assertEqual(view.func.view_class, DeleteDoneView)

    def test_logout_after(self):
        """Deleted user should be logged out after redirect."""
        user = self.response.context.get('user')
        self.assertIsInstance(user, AnonymousUser)

    def test_user_deleted(self):
        """User should be deleted at this point."""
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)
