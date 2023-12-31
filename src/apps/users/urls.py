from django.urls import path

from apps.users.api.views.auth_views import UserRegistrationView, UserLoginView
from apps.users.api.views.self_views import SelfView

urlpatterns = [
    path("me/", SelfView.as_view()),
    path("registration/", UserRegistrationView.as_view()),
    path("login/", UserLoginView.as_view()),
]
