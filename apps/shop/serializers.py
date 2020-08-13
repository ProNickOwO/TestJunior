from rest_framework import serializers

from apps.shop.models import Item


class ItemSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=399, required=False)
    sku = serializers.CharField(max_length=20, required=False)
    price = serializers.FloatField(required=False)
    description = serializers.CharField(required=False)

    class Meta:
        model = Item
        fields = ('id', 'name', 'sku', 'price', 'description', 'favorite_count')
