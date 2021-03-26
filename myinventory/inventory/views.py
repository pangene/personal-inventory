from django.shortcuts import render
from django.views.generic.list import ListView

from .models import Item


class ItemListView(ListView):
    model = Item
    paginate_by = 25

    def get_queryset(self):
        """Filter to only items associated with user."""
        queryset = Item.objects.filter(user=self.request.user)
        return queryset
