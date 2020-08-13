from django.contrib.auth.models import User
from django.db import models

from apps.shop.models import Item


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    name = models.CharField(max_length=399)
    items = models.ManyToManyField(Item, related_name='wishlist_items')
