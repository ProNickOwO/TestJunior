"""
Your app urls file
"""
from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.wishlists.views import AddToList, RemoveFromList, WishlistViewSet

router = DefaultRouter()
router.register(r'lists', WishlistViewSet, basename='lists')
urlpatterns = router.urls

urlpatterns = urlpatterns + [
    path('add/<int:list_id>/<int:item_id>', AddToList.as_view(), name='add item to list'),
    path('remove/<int:list_id>/<int:item_id>', RemoveFromList.as_view(), name='remove item from list'),
]
