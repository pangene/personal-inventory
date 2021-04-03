from django.test import TestCase

from ..models import EmailUser

class EmailUserManagerTests(TestCase):
    """Tests the custom email user manager."""

    def test_create_user(self):
        """Tests creating a new user with just email and password."""
        user = EmailUser.objects.create_user(email='bob@test.com', password='test')
        # field validation
        self.assertEqual(user.email, 'bob@test.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertIsNone(user.username)

        # errors properly
        with self.assertRaises(TypeError):
            EmailUser.objects.create_user()
        with self.assertRaises(TypeError):
            EmailUser.objects.create_user(email='')
        with self.assertRaises(ValueError):
            EmailUser.objects.create_user(email='', password='test')

    def test_create_superuser(self):
        superuser = EmailUser.objects.create_superuser('super@user.com', 'test')
        # field validation
        self.assertEqual(superuser.email, 'super@user.com')
        self.assertTrue(superuser.is_active)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
        self.assertIsNone(superuser.username)
        
        # cannot create superuser with improper permissions
        with self.assertRaises(ValueError):
            EmailUser.objects.create_superuser(email='super@user.com', password='test', 
                is_superuser=False)
        with self.assertRaises(ValueError):
            EmailUser.objects.create_superuser(email='super@user.com', password='test', 
                is_staff=False)
