from django.urls import path
from django.views.generic import TemplateView
from rest_framework import routers

from .views import ItemListView, ItemViewSet

urlpatterns = [
    path('', TemplateView.as_view(template_name='inventory/home.html'), name='home'),
    path('inventory', ItemListView.as_view(), name='inventory'),
]

# REST framework for the React home page.
router = routers.DefaultRouter()
router.register(r'api/items', ItemViewSet, basename='Item')

urlpatterns += router.urls
