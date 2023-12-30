from django.contrib import admin

from apps.users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "first_name", "last_name", "date_added")
    list_filter = ("id", "username", "email")
    search_fields = ("username", "email")
