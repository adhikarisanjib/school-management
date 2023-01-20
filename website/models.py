import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class Notice(models.Model):
    id = models.UUIDField(
        verbose_name=_("ID"),
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    subject = models.CharField(
        verbose_name=_("Subject"),
        max_length=511,
    )
    body = models.TextField(
        verbose_name=_("Body"),
        blank=True,
        null=True,
    )
    document = models.FileField(
        verbose_name=_("Document"),
        blank=True,
        null=True,
        upload_to="notices",
    )

    def __str__(self):
        return self.subject
