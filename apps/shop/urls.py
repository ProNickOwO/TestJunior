"""
Your app urls file
"""
from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.shop.views import RegisterUserView, LoginAPIView, LogoutAPIView, AddToList, RemoveFromList, ProductViewSet, \
    WishlistViewSet

router = DefaultRouter()
router.register(r'product', ProductViewSet, basename='product')
router.register(r'lists', WishlistViewSet, basename='lists')
urlpatterns = router.urls

urlpatterns = urlpatterns + [
    path('register/', RegisterUserView.as_view(), name='token_register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('add/<int:list_id>/<int:item_id>', AddToList.as_view(), name='add item to list'),
    path('remove/<int:list_id>/<int:item_id>', RemoveFromList.as_view(), name='remove item from list'),
]
