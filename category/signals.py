from django.core.exceptions import ValidationError
from django.db.models.signals import post_delete, pre_save, post_save
from django.dispatch.dispatcher import receiver
from category.models import Brand, upload_location_brandimage
from pytils.translit import slugify

@receiver(post_delete, sender=Brand)
def logo_delete(sender, instance, **kwargs):
    if instance.logo.name:
       instance.logo.delete(False)
    if instance.iso.name:
       instance.iso.delete(False)

@receiver(pre_save, sender=Brand)
def logo_add(sender, instance, **kwargs):
    print(instance.pk)
    if instance.pk is not None:
       old_self = sender.objects.get(pk=instance.pk)
       print(old_self.logo)
       print('-----------------------------------------')
       print(instance.logo)
       print('-----------------------------------------')
       print(kwargs)
       print('-----------------------------------------')
       if instance.logo != old_self.logo:
          print('1')
          old_self.logo.delete(False)
       if old_self.iso and instance.iso != old_self.iso:
          old_self.iso.delete(False)
       if instance.name != old_self.name:
          super(Brand, instance).save()
