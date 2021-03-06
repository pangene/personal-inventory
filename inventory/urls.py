from django.urls import path
from django.views.generic import TemplateView
from rest_framework import routers

from .views import ItemListView, ItemUpdateView, ItemViewSet, ItemDeleteView

urlpatterns = [
    path('', TemplateView.as_view(template_name='inventory/home.html'), name='home'),
    path('inventory/', ItemListView.as_view(), name='inventory'),
    path('items/<pk>/', ItemUpdateView.as_view(), name='item'),
    path('items/<pk>/delete/', ItemDeleteView.as_view(), name='item_delete')
]

# REST framework for the React home page.
router = routers.DefaultRouter()
router.register(r'api/items', ItemViewSet, basename='Item')

urlpatterns += router.urls
