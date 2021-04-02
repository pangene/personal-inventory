from django.test import TestCase
from django.urls import reverse, resolve
from django.utils.http import urlencode

from .setup import SetupTests
from inventory.views import ItemUpdateView
from inventory.models import Item


class ItemUpdateSetup(SetupTests):
    def setUp(self):
        super().setUp()
        self.first_item_name = list(self.items.keys())[0]
        self.first_item_tags = list(self.items.values())[0]


class ItemUpdateTests(ItemUpdateSetup):
    """Tests the item update view."""

    def setUp(self):
        super().setUp()
        url = reverse('item', args=[self.first_item_name])
        self.response = self.client.get(url)

    def test_status_code(self):
        """Tests item update page is viewable."""
        self.assertEqual(self.response.status_code, 200)

    def test_view_function(self):
        """Tests item update view directs properly."""
        view = resolve('/items/' + self.first_item_name + '/')
        self.assertEqual(view.func.view_class, ItemUpdateView)

    def test_contains_generic(self):
        """Tests the item update page contains all necessary components."""
        # Name, Upc, Quantity, Tags, Update button, Delete button
        self.assertContains(self.response, '<input', 6)


class SuccessfulItemUpdateTests(ItemUpdateSetup):
    """Tests successful post to item update view."""

    def setUp(self):
        super().setUp()
        url = reverse('item', args=[self.first_item_name])
        self.first_item_tags.append("cool")
        data = {
            'name': self.first_item_name,
            'upc': '',
            'quantity': 5,
            'tags': ", ".join(self.first_item_tags)
        }
        self.response = self.client.post(url, data)

    def test_item_updated(self):
        """Tests the item updates on successful post."""
        item = Item.objects.get(name=self.first_item_name)
        self.assertEqual(item.quantity, 5)
        item_tags = [tag.name for tag in item.tags.all()]
        self.assertEqual(set(item_tags), set(self.first_item_tags))


class InvalidItemUpdateTests(ItemUpdateSetup):
    """Tests invalid post to item update view."""

    def setUp(self):
        super().setUp()
        url = reverse('item', args=[self.first_item_name])
        data = {
            'name': '',
            'upc': '',
            'quantity': 0,
            'tags': ''
        }
        self.response = self.client.post(url, data)

    def test_item_not_updated(self):
        """Tests the item updates on invalid post."""
        item = Item.objects.get(name=self.first_item_name)
        self.assertEqual(item.quantity, 1)
        item_tags = [tag.name for tag in item.tags.all()]
        self.assertEqual(set(item_tags), set(self.first_item_tags))
