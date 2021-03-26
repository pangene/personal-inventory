from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('register/', views.SignUpView.as_view(), name='register'),
    path('delete/confirm/', views.DeleteConfirmView.as_view(), name='delete_confirm'),
    path('delete/done/', views.DeleteView.as_view(), name='delete'),
]
