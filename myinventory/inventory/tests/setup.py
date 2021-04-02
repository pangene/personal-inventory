from django.test import TestCase
from django.contrib.auth import get_user_model

from inventory.models import Item

User = get_user_model()


class SetupTests(TestCase):
    """Setup for the other tests in inventory/tests/"""

    def setUp(self):
        # Create new user
        self.email = 'test@test.com'
        self.password = 'cooltest'
        self.user = User.objects.create(email=self.email)
        self.user.set_password('cooltest')
        self.user.save()

        # Login
        self.client.login(email=self.email, password=self.password)

        # Create items
        self.items = { # 'item name': [tags list]
            "pikachu doll": ['cute', 'doll'],
            "percy jackson lightning thief": ['book', 'percy jackson'],
            "Django for dummies": ['book', 'programming', 'learning'],
            "detective pikachu": ['movie', 'kids']
        }
        for name, tags in self.items.items():
            item = Item.objects.create(user=self.user, name=name)
            item.tags.add(*tags)

        # Create a second user
        self.other_item_name = "<THIS ITEM SHOULDN'T BE VISIBLE>"
        self.second_user = User.objects.create(email="2@gmail.com")
        Item.objects.create(user=self.second_user, name=self.other_item_name)
