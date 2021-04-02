from django.test import TestCase
from django.urls import reverse, resolve

from .setup import SetupTests
from inventory.views import ItemListView

class InventoryListTests(SetupTests):
    """Tests for the inventory list view."""

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

    def test_contains_generic(self):
        """Tests inventory contains: search input, tags input, submit, table."""
        self.assertContains(self.response, "<input", 3)
        self.assertContains(self.response, "<table", 1)

    def test_contains_items(self):
        """Tests that it contains the right items."""
        for item, tags in self.items.items():
            self.assertContains(self.response, item)
            item_update_url = reverse('item', args=[item])
            self.assertContains(self.response, item_update_url)
            for tag in tags:
                self.assertContains(self.response, tag)

        # Shouldn't contain items from other users.
        self.assertNotContains(self.response, self.other_item_name)


class InventoryListSearchTests(SetupTests):
    """Tests for searching the inventory list view."""

    def setUp(self):
        super().setUp()
        self.url = reverse('inventory')

    def test_search_name(self):
        """Tests searching by name."""
        response = self.client.get(self.url + "?q=pikachu")
        # 3 <tr>'s: one for heading, two for two pikachu items
        self.assertContains(response, "<tr", 3)
        # 1 for search query + 2 for item names + 2 for item links
        self.assertContains(response, "pikachu", 5)

    def test_search_tag(self):
        """Tests searching by one tag."""
        response = self.client.get(self.url + "?q_tags=book")
        # 2 items again
        self.assertContains(response, "<tr", 3)
        # this time, extra book comes from JS function to add to tags input on click.
        self.assertContains(response, "book", 5)

    def test_search_multiple_tags(self):
        """Tests searching by multiple tags."""
        # %2C+ is how CSVs are separated in url search params
        response = self.client.get(self.url + "?q_tags=book%2C+programming")
        self.assertContains(response, "<tr", 2)
        self.assertContains(response, 'book', 3)
        self.assertContains(response, 'programming', 3)

    def test_search_name_tag(self):
        """Tests searching by both name and tag."""
        response = self.client.get(self.url + "?q=percy&q_tags=book")
        self.assertContains(response, "<tr", 2)
        self.assertContains(response, "percy jackson")
        self.assertNotContains(response, "Django")
