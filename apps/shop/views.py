# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from drf_util.decorators import serialize_decorator
from rest_framework import status, viewsets
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from apps.shop.models import Item, Wishlist
from apps.shop.serializers import ItemSerializer, RegisterSerializer, LoginSerializer, WishlistSerializer


class ProductViewSet(viewsets.ViewSet):
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        items = Item.objects.all()
        return Response(ItemSerializer(items, many=True).data)

    def create(self, request):
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            Item.objects.create(
                name=serializer.data['name'],
                sku=serializer.data['sku'],
                price=serializer.data['price'],
                description=serializer.data['description'],
            )
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        serializer = ItemSerializer(data=request.data)
        item = Item.objects.get(pk=pk)
        if serializer.is_valid():
            if 'name' in serializer.data:
                item.name = serializer.data['name']
            if 'sku' in serializer.data:
                item.sku = serializer.data['sku']
            if 'price' in serializer.data:
                item.price = serializer.data['price']
            if 'description' in serializer.data:
                item.description = serializer.data['description']
            item.save()

        return Response(serializer.data)

    def update(self, request, pk=None):
        serializer = ItemSerializer(data=request.data)
        item = Item.objects.get(pk=pk)
        if serializer.is_valid():
            if 'name' in serializer.data:
                item.name = serializer.data['name']
            if 'sku' in serializer.data:
                item.sku = serializer.data['sku']
            if 'price' in serializer.data:
                item.price = serializer.data['price']
            if 'description' in serializer.data:
                item.description = serializer.data['description']
            item.save()

        return Response(serializer.data)

    def destroy(self, request, pk=None):
        Item.objects.get(pk=pk).delete()

        return Response(status.HTTP_200_OK)


class WishlistViewSet(viewsets.ViewSet):
    serializer_class = WishlistSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        wlist = Wishlist.objects.filter(user=request.user)
        return Response(WishlistSerializer(wlist, many=True).data)

    def create(self, request):
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            wlist = Wishlist.objects.create(
                user=request.user,
                name=serializer.data['name'],
            )
            return Response(WishlistSerializer(wlist).data)
        else:
            return Response(status.HTTP_304_NOT_MODIFIED)

    def partial_update(self, request, pk=None):
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            wlist = Wishlist.objects.get(pk=pk, user=request.user)
            wlist.name = serializer.data['name']
            wlist.save()

            return Response(WishlistSerializer(wlist).data)
        else:
            return Response(status.HTTP_304_NOT_MODIFIED)

    def update(self, request, pk=None):
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            wlist = Wishlist.objects.get(pk=pk, user=request.user)
            wlist.name = serializer.data['name']
            wlist.save()

            return Response(WishlistSerializer(wlist).data)
        else:
            return Response(status.HTTP_304_NOT_MODIFIED)

    def destroy(self, request, pk=None):
        Wishlist.objects.get(pk=pk, user=request.user).delete()

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
