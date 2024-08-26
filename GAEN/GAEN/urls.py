from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static

schema_view = get_schema_view(
    openapi.Info(
        title="GAEN",
        default_version='v1',
        description="Global Art Exchange Network",
        terms_of_service="url",
        contact=openapi.Contact(email="muxtorovshaxzodbek16@gmail.com"),
        license=openapi.License(name="MIT LICENSE"),
    ),
    public=False,
    permission_classes=[permissions.IsAuthenticatedOrReadOnly],
)

urlpatterns = [
    path('_admin/_gaen/', admin.site.urls),

    path('api/v1/__/auth/', include("userAuth.urls")),
    path('api/v1/__/auth/', include('socialAuth.urls')),
    path('api/v1/__/article/user/', include('art.urls')),
    path('api/v1/article/__/admin/', include('art.adminUrls')),

    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redocs/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
