from django.db import models
from django.contrib.auth import get_user_model

from taggit.managers import TaggableManager

User = get_user_model()

class Item(models.Model):
    user = models.ForeignKey(User,
        on_delete=models.CASCADE,
        related_name='items'
    )
    name = models.CharField(max_length=100, primary_key=True)
    upc = models.CharField(max_length=12, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    date_added = models.DateField(auto_now_add=True)
    tags = TaggableManager()

    def __str__(self):
        return self.name
