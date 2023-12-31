from django.contrib import admin
from django.urls import include, path, re_path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView, TokenVerifyView)
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Vocabulary API",
        default_version='v1',
        description="Documentation for my API",
        contact=openapi.Contact(email="contact.yuriidorosh@gmail.com"),
        license=openapi.License(name="MIT"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


API_PATH = "api/v1/"

urlpatterns = [
    path("admin/", admin.site.urls),
    path(f"{API_PATH}token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path(f"{API_PATH}token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path(f"{API_PATH}token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path(f"{API_PATH}users/", include("apps.users.urls")),
    re_path(API_PATH + r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path(f'{API_PATH}swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path(f'{API_PATH}redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
