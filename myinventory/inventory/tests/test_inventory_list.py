from django.test import TestCase
from django.urls import reverse, resolve

from .setup import SetupTests
from inventory.views import ItemListView

class InventoryListTests(SetupTests):
    """Test for the inventory list view."""

    def setUp(self):
        super().setUp()
        url = reverse('inventory')
        self.response = self.client.get(url)

    def test_status_code(self):
        """Tests inventory list page is viewable."""
        self.assertEqual(self.response.status_code, 200)

    def test_view_function(self):
        """Tests inventory list view directs properly."""
        view = resolve('/inventory/')
        self.assertEqual(view.func.view_class, ItemListView)
