from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

from taggit.managers import TaggableManager
from taggit.models import CommonGenericTaggedItemBase, TaggedItemBase

User = get_user_model()

class GenericStringTaggedItem(CommonGenericTaggedItemBase, TaggedItemBase):
    object_id = models.CharField(max_length=50, verbose_name='Object id', db_index=True)


class Item(models.Model):
    user = models.ForeignKey(User,
        on_delete=models.CASCADE,
        related_name='items'
    )
    name = models.CharField(max_length=100, primary_key=True)
    upc = models.CharField(max_length=12, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True)
    tags = TaggableManager(through=GenericStringTaggedItem, blank=True)

    def __str__(self):
        return self.name
