from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, DeleteView
from rest_framework import viewsets, filters
from taggit.forms import TagField
from django import forms

from .models import Item
from .serializers import ItemSerializer


class ItemListView(ListView):
    """List view to examine the user inventory."""
    model = Item
    paginate_by = 13

    def get_queryset(self):
        """Filter based off user and search parameters."""
        # Filter off user
        queryset = Item.objects.filter(user=self.request.user)

        # Filter off query params.
        name_query = self.request.GET.get('q')
        if name_query:
            queryset = queryset.filter(name__icontains=name_query)
        tags_query = self.request.GET.get('q_tags')
        if tags_query:
            tags = tags_query.split(",")
            tags = list(map(lambda x: x.strip(), tags))
            for tag in tags:
                # Filtering by tags__name__in=[tags list] results in objects with any of the tags.
                queryset = queryset.filter(tags__name__icontains=tag)
                print(queryset)
        return queryset


class ItemUpdateView(UpdateView):
    """Update view to examine and update an individual item."""
    model = Item
    template_name_suffix = '_update'
    fields = ['name', 'upc', 'quantity', 'tags']

    success_url = reverse_lazy('inventory')


class ItemDeleteView(DeleteView):
    """Delete view to delete the item."""
    model = Item
    success_url = reverse_lazy('inventory')


class ItemViewSet(viewsets.ModelViewSet):
    """Viewset so React frontend can interact with items api."""
    serializer_class = ItemSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', '=upc']

    def get_queryset(self):
        queryset = self.request.user.items.all()
        name = self.request.query_params.get('name')
        if name is not None:
            queryset = queryset.filter(name=name)
        return queryset
