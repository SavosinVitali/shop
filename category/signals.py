from typing import List, Tuple

from django.core.exceptions import ValidationError
from django.db.models.signals import post_delete, pre_save, post_save
from django.dispatch.dispatcher import receiver
from category.models import Brand, upload_location_image
from pytils.translit import slugify
import os
from django.conf import settings
from PIL import Image
from sorl.thumbnail import get_thumbnail

@receiver(post_delete, sender=Brand)
def logo_delete(sender, instance, **kwargs):
    if instance.logo.name:
       print('post_delete')
       instance.logo.delete(False)
    if instance.iso.name:
       instance.iso.delete(False)

@receiver(pre_save, sender=Brand)
def logo_add(sender, instance, **kwargs):
    if instance.pk is not None:
       old_self = sender.objects.get(pk=instance.pk)
       if old_self.logo and instance.logo != old_self.logo:
           filebase, extension = old_self.logo.name.split('.')
           sizes = [(240, 240), (960, 960)]
           old_self.logo.delete(False)
           for size in sizes:
               name = settings.MEDIA_ROOT + '\%s_%s.%s' % (filebase, size[0], extension)
               if os.path.isfile(name):
                   os.remove(name)
       if old_self.iso and instance.iso != old_self.iso:
          old_self.iso.delete(False)
       if instance.name != old_self.name and os.path.isfile(settings.MEDIA_ROOT + '\\' + instance.logo.name):
          new_path = upload_location_image(instance, instance.logo.name)
          os.rename(settings.MEDIA_ROOT + '\\' + instance.logo.name, settings.MEDIA_ROOT + '\\' + new_path)
          instance.logo = new_path


@receiver(post_save, sender=Brand)
def resize_image(sender, instance, **kwargs):
    print('-resize-')
    if instance.pk is not None and instance.logo:
        filebase, extension = instance.logo.name.split('.')
        sizes = [(240, 240), (960, 960)]
        for size in sizes:
            im = Image.open(instance.logo)
            name = settings.MEDIA_ROOT + '\%s_%s.%s' % (filebase, size[0], extension)
            im.thumbnail(size)
            im.save(name)

