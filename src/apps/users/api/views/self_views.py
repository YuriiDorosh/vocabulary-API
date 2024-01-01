from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from apps.users.api.serializers.user_serializers import UserSerializer
from apps.users.models import User


class SelfView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self) -> User:
        return self.request.user


