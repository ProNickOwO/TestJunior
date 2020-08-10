# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from drf_util.decorators import serialize_decorator
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.shop.models import Item, Wishlist
from apps.shop.serializers import ItemSerializer, RegisterSerializer, LoginSerializer, WishlistSerializer


class ProductsView(GenericAPIView):
    serializer_class = ItemSerializer

    def get(self, request):
        items = Item.objects.all()
        return Response(ItemSerializer(items, many=True).data)


class AddItem(GenericAPIView):
    serializer_class = ItemSerializer

    @serialize_decorator(ItemSerializer)
    def post(self, request):
        validated_data = request.serializer.validated_data

        item = Item.objects.create(
            name=validated_data['name'],
            sku=validated_data['sku'],
            price=validated_data['price'],
            description=validated_data['description'],
        )
        return Response(ItemSerializer(item).data)


class ChangeItem(GenericAPIView):
    serializer_class = ItemSerializer

    @serialize_decorator(ItemSerializer)
    def patch(self, request, item_id):
        validated_data = request.serializer.validated_data

        item = Item.objects.get(pk=item_id)
        if 'name' in validated_data:
            item.name = validated_data['name']
        if 'sku' in validated_data:
            item.sku = validated_data['sku']
        if 'price' in validated_data:
            item.price = validated_data['price']
        if 'description' in validated_data:
            item.description = validated_data['description']
        item.save()

        return Response(ItemSerializer(item).data)


class DeleteItem(GenericAPIView):

    def get(self, request, item_id):
        Item.objects.get(pk=item_id).delete()

        return Response(status.HTTP_200_OK)


class WishlistsView(GenericAPIView):
    serializer_class = WishlistSerializer

    def get(self, request):
        wlist = Wishlist.objects.filter(user=request.user)
        return Response(WishlistSerializer(wlist, many=True).data)


class AddList(GenericAPIView):
    serializer_class = WishlistSerializer

    @serialize_decorator(WishlistSerializer)
    def post(self, request):
        validated_data = request.serializer.validated_data

        wlist = Wishlist.objects.create(
            user=request.user,
            name=validated_data['name'],
        )
        return Response(WishlistSerializer(wlist).data)


class ChangeList(GenericAPIView):
    serializer_class = WishlistSerializer

    @serialize_decorator(WishlistSerializer)
    def patch(self, request, list_id):
        validated_data = request.serializer.validated_data

        wlist = Wishlist.objects.get(pk=list_id, user=request.user)
        wlist.name = validated_data['name']
        wlist.save()

        return Response(WishlistSerializer(wlist).data)


class DeleteList(GenericAPIView):

    def get(self, request, list_id):
        Wishlist.objects.get(pk=list_id, user=request.user).delete()

        return Response(status.HTTP_200_OK)


class AddToList(GenericAPIView):

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

    def get(self, request, list_id, item_id):
        wlist = Wishlist.objects.get(pk=list_id, user=request.user)
        item = Item.objects.get(pk=item_id)
        wlist.items.remove(item)
        if not Wishlist.objects.filter(user=request.user).filter(items=item).exists():
            item.favorite_count = item.favorite_count - 1
            item.save()
        wlist.save()
        return Response(WishlistSerializer(wlist).data)


class RegisterUserView(GenericAPIView):
    serializer_class = RegisterSerializer

    permission_classes = (AllowAny,)
    authentication_classes = ()

    @serialize_decorator(RegisterSerializer)
    def post(self, request):
        validated_data = request.serializer.validated_data

        user = User.objects.create(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            username=validated_data['username'],
            email=validated_data['email'],
            is_superuser=True,
            is_staff=True
        )
        user.set_password(validated_data['password'])
        user.save()
        return Response(RegisterSerializer(user).data)


class LoginAPIView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    @serialize_decorator(LoginSerializer)
    def post(self, request):
        validated_data = request.serializer.validated_data

        username = validated_data['username']
        password = validated_data['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return Response(LoginSerializer(user).data, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_401_UNAUTHORIZED)


class LogoutAPIView(GenericAPIView):
    permission_classes = [AllowAny]

    def get(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)
