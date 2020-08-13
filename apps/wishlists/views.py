from rest_framework import viewsets
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.shop.models import Item, Wishlist
from apps.wishlists.serializers import Empty
from apps.wishlists.serializers import WishlistSerializer


class WishlistViewSet(viewsets.ModelViewSet):
    serializer_class = WishlistSerializer
    permission_classes = [IsAuthenticated]
    queryset = Wishlist.objects.all()

    def get_queryset(self):
        user = self.request.user
        return Wishlist.objects.filter(user=user)

    def create(self, request, *args, **kwargs):
        request.data['user'] = request.user
        Wishlist.objects.create(**request.data)
        return Response(request.data)


class AddToList(GenericAPIView):
    serializer_class = Empty

    def get(self, request, list_id, item_id):
        wlist = Wishlist.objects.get(pk=list_id, user=request.user)
        item = Item.objects.get(pk=item_id)
        if not Wishlist.objects.filter(user=request.user).filter(items=item).exists():
            item.favorite_count = item.favorite_count + 1
            item.save()
        wlist.items.add(item)
        wlist.save()
        return Response(WishlistSerializer(wlist).data)


class RemoveFromList(GenericAPIView):
    serializer_class = Empty

    def get(self, request, list_id, item_id):
        wlist = Wishlist.objects.get(pk=list_id, user=request.user)
        item = Item.objects.get(pk=item_id)
        wlist.items.remove(item)
        if not Wishlist.objects.filter(user=request.user).filter(items=item).exists():
            item.favorite_count = item.favorite_count - 1
            item.save()
        wlist.save()
        return Response(WishlistSerializer(wlist).data)
