import os

from django.conf import settings
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver

from base.models import User


@receiver(pre_delete, sender=User)
def account_delete(sender, instance, **kwargs):
    """
    Deleting the specific image of a Post after delete it
    """
    if instance.avatar and instance.avatar != "default/dummy_image.png":
        if os.path.isfile(instance.avatar.path):
            os.remove(instance.avatar.path)
            os.rmdir(settings.BASE_DIR / f"media/{instance.id}/avatars")


@receiver(pre_save, sender=User)
def account_update(sender, instance, **kwargs):
    """
    Replacing the specific image of a Post after update
    """

    try:
        old_avatar = sender.objects.get(id=instance.id).avatar
        new_avatar = instance.avatar
        if not (old_avatar == new_avatar or old_avatar == "default/dummy_image.png"):
            if os.path.isfile(old_avatar.path):
                os.remove(old_avatar.path)
    except Exception:
        return
