from django.test import TestCase
from django.urls import reverse, resolve

from .setup import SetupTests
from inventory.views import ItemDeleteView
from inventory.models import Item


class ItemDeleteTests(SetupTests):
    """Tests for item deletion view."""

    def setUp(self):
        super().setUp()
        self.first_item_name = list(self.items.keys())[0]
        self.first_item_tags = list(self.items.values())[0]
        self.url = reverse('item_delete', args=[self.first_item_name])
        self.response = self.client.get(self.url)

    def test_status_code(self):
        """Tests item delete page is viewable."""
        self.assertEqual(self.response.status_code, 200)

    def test_view_function(self):
        """Tests item delete view directs properly."""
        view = resolve('/items/' + self.first_item_name.replace(' ', '%20') + '/delete/')
        self.assertEqual(view.func.view_class, ItemDeleteView)

    def test_contains_generic(self):
        """Tests the item delete page contains all necessary components."""
        # CSRF, Delete button
        self.assertContains(self.response, '<input', 2)

    def test_deletes_and_redirects(self):
        """Tests the item deletes and page redirects upon confirmation."""
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse('inventory'))
        self.assertRaises(Item.DoesNotExist, lambda: Item.objects.get(name=self.first_item_name))
