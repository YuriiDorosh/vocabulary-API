from typing import Any

from rest_framework import permissions
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from django.core.exceptions import ImproperlyConfigured
from django.db.models import QuerySet

from apps.users.api.serializers import UserSerializer
from apps.users.models import User



# class SelfView(GenericAPIView):
#     serializer_class = UserSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, *args: Any) -> Response:
#         user = self.get_object()
#         serializer = self.get_serializer(user)

#         return Response(serializer.data)

#     def patch(self, request: Request) -> Response:
#         user_updater = UserUpdater(
#             user=self.get_object(),
#             user_data=request.data,
#         )

#         user = user_updater()

#         return Response(
#             self.get_serializer(user).data,
#         )

#     def get_object(self) -> User:
#         return self.request.user

#     def get_queryset(self) -> QuerySet[User]:
#         return User.objects.filter(is_active=True)

from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

class SelfView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self) -> User:
        return self.request.user

    def get_queryset(self):
        return User.objects.filter(is_active=True)