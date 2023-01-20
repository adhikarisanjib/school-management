import time
import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from administrator.models import Assign, Student


class Attendence(models.Model):
    id = models.UUIDField(
        verbose_name=_("ID"),
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    assign = models.ForeignKey(
        Assign,
        on_delete=models.PROTECT,
    )
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
    )
    date = models.DateField(
        verbose_name=_("Date"),
        auto_now_add=True,
    )
    is_present = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return f"{self.student.user.name} {self.is_present}"
