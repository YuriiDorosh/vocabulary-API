from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


def create_jwt_pair_for_user(user: User) -> dict[str]:
    refresh = RefreshToken.for_user(user)

    tokens = {
        "refresh": str(refresh),
        "access": str(refresh.access_token), 
        }

    return tokens