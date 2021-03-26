from django.urls import path
from django.views.generic import TemplateView

from .views import ItemListView

urlpatterns = [
    path('', TemplateView.as_view(template_name='inventory/home.html'), name='home'),
    path('inventory', ItemListView.as_view(), name='inventory')
]
