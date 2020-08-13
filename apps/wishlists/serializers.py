from django.contrib.auth.models import User
from rest_framework import serializers

from apps.shop.models import Wishlist
from apps.shop.serializers import ItemSerializer


class WishlistSerializer(serializers.ModelSerializer):
    user = User
    name = serializers.CharField(max_length=399, required=True)
    items = ItemSerializer(many=True, required=False)

    class Meta:
        model = Wishlist
        fields = ('id', 'name', 'items')


class Empty(serializers.Serializer):
    pass
