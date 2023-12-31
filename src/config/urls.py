from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView, TokenVerifyView)

API_PATH = "api/v1/"

urlpatterns = [
    path("admin/", admin.site.urls),
    path(f"{API_PATH}token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path(f"{API_PATH}token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path(f"{API_PATH}token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path(f"{API_PATH}users/", include("apps.users.urls")),
]
