# Create your views here.
from rest_framework import viewsets
from rest_framework.mixins import DestroyModelMixin, ListModelMixin, CreateModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated

from apps.shop.models import Item
from apps.shop.serializers import ItemSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]
