from django.db import models
from django.contrib.auth.models import User

class Item(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, 
        related_name='items')
    name = models.CharField(max_length=100)
    upc = models.CharField(max_length=12, null=True)
    isbn = models.CharField(max_length=13, null=True)
