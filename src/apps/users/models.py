import uuid

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password, **extra_fields):
        if not email:
            raise ValueError(_("The Email field must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    class GENDERS(models.TextChoices):
        MALE = "male", _("Male")
        FEMALE = "female", _("Female")

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, db_index=True
    )
    email = models.EmailField(unique=True)
    username = models.CharField(_("username"), unique=True, max_length=30)
    first_name = models.CharField(_("first name"), max_length=30, blank=True)
    last_name = models.CharField(_("last name"), max_length=30, blank=True)
    gender = models.CharField(
        _("Gender"), max_length=12, choices=GENDERS.choices, blank=True
    )
    date_added = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        db_table = "vocabulary_users"
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self) -> str:
        if self.first_name and self.last_name:
            name = f"{self.first_name} {self.last_name}"
        else:
            name = self.username

        return name.strip()

    @classmethod
    def parse_name(cls, name: str) -> dict:
        parts = name.split(" ", 2)

        if len(parts) == 1:
            return {"first_name": parts[0]}

        if len(parts) == 2:
            return {"first_name": parts[0], "last_name": parts[1]}

        return {"first_name": parts[0], "last_name": " ".join(parts[1:])}
