"""
Your app urls file
"""
from django.urls import path

from apps.first_app.views import ProductsView, RegisterUserView, LoginAPIView, LogoutAPIView, AddItem, ChangeItem, \
    DeleteItem

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='token_register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('all_items', ProductsView.as_view(), name='all items'),
    path('add_item', AddItem.as_view(), name='create item'),
    path('change_item/<int:item_id>', ChangeItem.as_view(), name='change item'),
    path('delete_item/<int:item_id>', DeleteItem.as_view(), name='delete item'),
]
