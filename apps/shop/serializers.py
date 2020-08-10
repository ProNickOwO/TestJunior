from django.contrib.auth.models import User
from rest_framework import serializers

from apps.shop.models import Item


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('name', 'sku', 'price', 'description', 'favorite_count')


class WishlistSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True)

    class Meta:
        model = Item
        fields = ('name', 'items')


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "username", "password",)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=399)
    password = serializers.CharField(max_length=399, write_only=True)


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = User
        fields = '__all__'
