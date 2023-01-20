import uuid

from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    Group,
    Permission,
    _user_get_permissions,
    _user_has_module_perms,
    _user_has_perm,
)
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


class UserTypeManager(models.Manager):
    use_in_migrations = True

    def get_by_natural_key(self, name):
        return self.get(name=name)


class UserType(models.Model):
    id = models.UUIDField(
        verbose_name=_("ID"),
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    name = models.CharField(
        _("name"),
        max_length=31,
        unique=True,
    )
    permissions = models.ManyToManyField(
        Permission,
        verbose_name=_("permissions"),
        blank=True,
    )

    objects = UserTypeManager()

    def __str__(self):
        return self.name

    def natural_key(self):
        return (self.name,)


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("User must have an email address.")
        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email=email,
            password=password,
        )
        user.is_superuser = True
        user.is_staff = True
        user.is_email_verified = True
        user.save(using=self._db)
        return user


def get_user_avatar(user, filename):
    return f"{user.id}/avatars/{filename}"


def get_default_avatar():
    return "default/dummy_image.png"


def get_email_verified_value():
    if settings.DEBUG:
        return True
    return False


class User(AbstractBaseUser):
    id = models.UUIDField(
        verbose_name=_("ID"),
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    email = models.EmailField(
        verbose_name=_("Email"),
        max_length=127,
        unique=True,
        error_messages={
            "null": _("Email field is required."),
            "unique": _("An account with that email already exists. Please login to continue."),
            "invalid": _("Enter a valid email address."),
        },
    )
    username = models.CharField(
        verbose_name=_("Username"),
        max_length=127,
        unique=True,
        error_messages={
            "null": _("Username field is required."),
            "unique": _("An account with that username already exists."),
            "invalid": _("Enter a valid username."),
        },
        help_text=_("Better to use your email address all characters before @."),
    )
    user_type = models.ForeignKey(
        UserType,
        on_delete=models.SET_NULL,
        related_name="user_type",
        null=True,
        blank=True,
    )
    name = models.CharField(
        verbose_name=_("Full Name"),
        max_length=255,
        null=True,
        blank=True,
    )
    contact_number = PhoneNumberField(
        verbose_name=_("Contact Number"),
        null=True,
        blank=True,
    )
    avatar = models.ImageField(
        verbose_name=_("Avatar"),
        blank=True,
        null=True,
        default=get_default_avatar,
        upload_to=get_user_avatar,
    )
    is_email_verified = models.BooleanField(
        verbose_name=_("Email Verification Status"),
        default=get_email_verified_value,
        help_text=_("Designates whether this user is verified or not."),
    )
    is_staff = models.BooleanField(
        verbose_name=_("Staff Status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        verbose_name=_("Active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active."
            "Unselect this field instead of deleting accounts."
        ),
    )
    is_superuser = models.BooleanField(
        _("superuser status"),
        default=False,
        help_text=_("Designates that this user has all permissions without explicitly assigning them."),
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_("user permissions"),
        blank=True,
        help_text=_("Specific permissions for this user."),
        related_name="user_set",
        related_query_name="user",
    )
    groups = models.ManyToManyField(
        Group,
        verbose_name=_("Groups"),
        blank=True,
        help_text=_(
            "The groups this user belongs to. A user will get all permissions granted to each of their groups."
        ),
        related_name="user_set",
        related_query_name="user",
    )
    last_login = models.DateTimeField(
        verbose_name=_("Last Login"),
        auto_now=True,
    )
    date_joined = models.DateTimeField(
        verbose_name=_("Date Joined"),
        auto_now_add=True,
        editable=False,
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        ordering = ["-date_joined"]

    def __str__(self):
        return self.username

    def get_avatar_name(self):
        return str(self.avatar)[str(self.avatar).index(f"{self.id}/avatars/") :]

    def get_fields_and_values(self):
        user = [
            ("id", self.id),
            ("email", self.email),
            ("username", self.username),
            ("user_type", self.user_type),
            ("name", self.name),
            ("contact_number", self.contact_number),
            ("avatar", self.avatar),
            ("is_email_verified", self.is_email_verified),
            ("is_active", self.is_active),
            ("last_login", self.last_login),
            ("date_joined", self.date_joined),
        ]
        return user

    # Helper methods for user permissions as defined in django.contrib.auth.models
    def get_user_permissions(self, obj=None):
        return _user_get_permissions(self, obj, "user")

    def get_user_type_permissions(self, obj=None):
        return _user_get_permissions(self, obj, "user_type")

    def get_all_permissions(self, obj=None):
        return _user_get_permissions(self, obj, "all")

    def has_perm(self, perm, obj=None):
        if self.is_active and self.is_superuser:
            return True
        return _user_has_perm(self, perm, obj)

    def has_perms(self, perm_list, obj=None):
        return all(self.has_perm(perm, obj) for perm in perm_list)

    def has_module_perms(self, app_label):
        if self.is_active and self.is_superuser:
            return True
        return _user_has_module_perms(self, app_label)
