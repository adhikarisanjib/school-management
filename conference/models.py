import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from base.models import User


class RoomMember(models.Model):
    id = models.UUIDField(
        verbose_name=_("ID"),
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    uid = models.CharField(
        verbose_name=_("User Number"),
        max_length=1023,
    )
    room_name = models.CharField(
        verbose_name=_("Room"),
        max_length=63,
    )
    in_session = models.BooleanField(
        default=True,
    )

    def __self__(self):
        return self.room_name
