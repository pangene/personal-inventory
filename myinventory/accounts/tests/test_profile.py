from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model

from ..views import ProfileView


User = get_user_model()


class ProfileTests(TestCase):
    """Tests the ProfileView."""

    def setUp(self):
        # Creating account and logging in
        email = 'test@test.com'
        password = 'cooltest'
        self.user = User.objects.create(email=email)
        self.user.set_password('cooltest')
        self.user.save()
        self.client.login(email=email, password=password)

        # Going to profile
        url = reverse('profile')
        self.response = self.client.get(url)

    def test_status_code(self):
        """Should be visible to logged in users."""
        self.assertEqual(self.response.status_code, 200)

    def test_profile_url_resolves(self):
        """Profile url should resolve to ProfileView."""
        view = resolve('/accounts/profile/')
        self.assertEqual(view.func.view_class, ProfileView)

    def test_contains_links(self):
        """Profile should contain way to change password and delete account."""
        password_change_url = reverse('password_change')
        delete_url = reverse('delete_confirm')
        self.assertContains(self.response, password_change_url)
        self.assertContains(self.response, delete_url)
