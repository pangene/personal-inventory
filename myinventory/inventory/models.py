from django.db import models
from django.contrib.auth import get_user_model

from taggit.managers import TaggableManager

User = get_user_model()

class Item(models.Model):
    user = models.ForeignKey(User, 
        on_delete=models.CASCADE, 
        related_name='items'
    )
    name = models.CharField(max_length=100)
    upc = models.CharField(max_length=12, null=True)
    tags = TaggableManager()
