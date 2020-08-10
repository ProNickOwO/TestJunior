"""
Your ROOT url file
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('common/', include('apps.common.urls')),
    path('shop/', include('apps.shop.urls')),
    path('auth-token', jwt_views.TokenObtainPairView.as_view()),  # auth endpoint
    path('auth-token/refresh', jwt_views.TokenRefreshView.as_view()),  # token refresh endpoint
]
