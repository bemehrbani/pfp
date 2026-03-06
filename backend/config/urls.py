"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from .views import health_check, simple_health

# Swagger/OpenAPI documentation
schema_view = get_schema_view(
    openapi.Info(
        title="PFP Campaign Manager API",
        default_version='v1',
        description="API documentation for People for Peace Campaign Manager",
        terms_of_service="https://www.peopleforpeace.org/terms/",
        contact=openapi.Contact(email="dev@peopleforpeace.org"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    # Admin panel
    path('admin/', admin.site.urls),

    # API documentation
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # Health checks
    path('health/', health_check, name='health-check'),
    path('health/simple/', simple_health, name='simple-health'),

    # API endpoints (to be added by each app)
    path('api/auth/', include('apps.users.api.urls')),
    path('api/campaigns/', include('apps.campaigns.api.urls')),
    path('api/tasks/', include('apps.tasks.api.urls')),
    path('api/analytics/', include('apps.analytics.api.urls')),
    path('api/telegram/', include('apps.telegram.api.urls')),
]

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)