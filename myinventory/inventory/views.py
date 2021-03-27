from django.shortcuts import render
from django.views.generic.list import ListView

from .models import Item


class ItemListView(ListView):
    model = Item
    paginate_by = 15

    def get_queryset(self):
        """Filter based off user and search parameters."""
        # Filter off user
        queryset = Item.objects.filter(user=self.request.user)

        # Filter off search params
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(name__icontains=query)
        return queryset
