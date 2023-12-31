from apps.users.api.serializers import UserSerializer
from apps.users.models import User


from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated


class SelfView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self) -> User:
        return self.request.user

    def get_queryset(self):
        return User.objects.filter(is_active=True)
