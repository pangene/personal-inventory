from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Item(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='items'
    )
    name = models.CharField(max_length=100)
    upc = models.CharField(max_length=12, null=True)
