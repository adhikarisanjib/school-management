from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from base.models import User, UserType


class UserAdmin(BaseUserAdmin):
    list_display = ("email", "username", "date_joined", "is_superuser", "is_staff", "is_email_verified")
    readonly_fields = ("id", "date_joined", "last_login", "is_superuser", "is_staff")
    search_fields = ("email", "username")
    list_filter = ()
    filter_horizontal = ()
    fieldsets = ()


admin.site.register(User, UserAdmin)
admin.site.register(UserType)
admin.site.unregister(Group)
