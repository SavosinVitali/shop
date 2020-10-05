from django.core.exceptions import ValidationError
from django.db.models.signals import post_delete, pre_save, post_save
from django.dispatch.dispatcher import receiver
from category.models import Brand, upload_location_brandimage
from pytils.translit import slugify
import os
from django.conf import settings

@receiver(post_delete, sender=Brand)
def logo_delete(sender, instance, **kwargs):
    if instance.logo.name:
       instance.logo.delete(False)
    if instance.iso.name:
       instance.iso.delete(False)

@receiver(pre_save, sender=Brand)
def logo_add(sender, instance, **kwargs):
    if instance.pk is not None:
       old_self = sender.objects.get(pk=instance.pk)
       if instance.logo != old_self.logo:
          old_self.logo.delete(False)
       if old_self.iso and instance.iso != old_self.iso:
          old_self.iso.delete(False)
       if instance.name != old_self.name:
          new_path = upload_location_brandimage(instance, instance.logo.name)
          os.rename(settings.MEDIA_ROOT  + '\\' + instance.logo.name, settings.MEDIA_ROOT  + '\\' + new_path)
          instance.logo = new_path

