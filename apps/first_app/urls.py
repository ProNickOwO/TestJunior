"""
Your app urls file
"""
from django.urls import path

from apps.first_app.views import ProductsView, RegisterUserView, LoginAPIView, LogoutAPIView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='token_register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('all_items', ProductsView.as_view(), name='all items'),
]
