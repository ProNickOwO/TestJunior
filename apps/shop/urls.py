"""
Your app urls file
"""
from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.shop.views import ProductViewSet

router = DefaultRouter()
router.register(r'product', ProductViewSet, basename='product')
urlpatterns = router.urls

urlpatterns = urlpatterns + [

]
