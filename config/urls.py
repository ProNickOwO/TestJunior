"""
Your ROOT url file
"""
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_simplejwt import views as jwt_views

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

urlpatterns += [
    path('admin/', admin.site.urls),
    path('common/', include('apps.common.urls')),
    path('products/', include('apps.shop.urls')),
    path('lists/', include('apps.wishlists.urls')),
    path('auth-token', jwt_views.TokenObtainPairView.as_view()),  # auth endpoint
    path('auth-token/refresh', jwt_views.TokenRefreshView.as_view()),  # token refresh endpoint
]
