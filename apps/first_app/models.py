from django.contrib.auth.models import User
from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=399)

    price = models.FloatField(default=0)
    description = models.TextField()
    favorite_count = models.IntegerField(default=0)


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=399)
    items = models.ManyToManyField(Item)
