# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from drf_util.decorators import serialize_decorator
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.first_app.models import Item
from apps.first_app.serializers import ItemSerializer, RegisterSerializer, LoginSerializer


class ProductsView(GenericAPIView):
    serializer_class = ItemSerializer

    def get(self, request):
        items = Item.objects.all()
        return Response(ItemSerializer(items).data)


class AddItem(GenericAPIView):
    serializer_class = ItemSerializer

    @serialize_decorator(ItemSerializer)
    def post(self, request):
        validated_data = request.serializer.validated_data

        item = Item.objects.create(
            name=validated_data['name'],
            price=validated_data['price'],
            description=validated_data['description'],
        )
        return Response(ItemSerializer(item).data)


class ChangeItem(GenericAPIView):
    serializer_class = ItemSerializer

    @serialize_decorator(ItemSerializer)
    def patch(self, request, item_id):
        validated_data = request.serializer.validated_data

        item, _ = Item.objects.get_or_create(pk=item_id)
        item.name = validated_data['name']
        item.price = validated_data['price']
        item.description = validated_data['description']
        item.save()

        return Response(ItemSerializer(item).data)


class DeleteItem(GenericAPIView):

    def get(self, request, item_id):
        Item.objects.get(pk=item_id).delete()

        return Response(status.HTTP_200_OK)


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
