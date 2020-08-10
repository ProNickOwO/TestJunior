"""
Your app urls file
"""
from django.urls import path

from apps.shop.views import *

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='token_register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('all_items/', ProductsView.as_view(), name='all items'),
    path('add_item/', AddItem.as_view(), name='create item'),
    path('change_item/<int:item_id>', ChangeItem.as_view(), name='change item'),
    path('delete_item/<int:item_id>', DeleteItem.as_view(), name='delete item'),
    path('all_lists/', WishlistsView.as_view(), name='all lists'),
    path('add_list/', AddList.as_view(), name='create list'),
    path('change_list/<int:list_id>', ChangeList.as_view(), name='change list'),
    path('delete_list/<int:list_id>', DeleteList.as_view(), name='delete list'),
    path('add/<int:list_id>/<int:item_id>', AddToList.as_view(), name='add item to list'),
    path('remove/<int:list_id>/<int:item_id>', RemoveFromList.as_view(), name='remove item from list'),
]
