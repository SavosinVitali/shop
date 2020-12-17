from django.db.models.signals import post_delete, pre_save, post_save
from django.dispatch.dispatcher import receiver
from file_storage.models import File_Storage, upload_location_file, Image_Storage, upload_location_image
import os
from django.conf import settings

# def file_rename_1(instance):
#     print('file_rename 1')
#     print(instance.files.url)
#     names = upload_location_file(instance, instance.files.url)
#     instance.files.close()
#     if os.path.isfile(settings.MEDIA_ROOT + '/' + instance.files.name):
#         print(settings.MEDIA_ROOT + '/' + instance.files.name)
#         print(settings.MEDIA_ROOT + '/' + names)
#         instance.files.close()
#         os.renames(settings.MEDIA_ROOT + '/' + instance.files.name, settings.MEDIA_ROOT + '/' + names)
#         print('22222222222222222222222222222222222222222222222222222')
#         instance.files = names




@receiver(pre_save, sender = File_Storage)
def file_rename(sender, instance, **kwargs):
    if instance.pk is not None:
        old_self = sender.objects.get(pk=instance.pk)
        # если поменялось название и не изменился файл
        # if old_self.title_files and instance.title_files != old_self.title_files and old_self.files == instance.files or \
        #     instance.file_type != old_self.file_type and old_self.files == instance.files:
        names = upload_location_file(instance, old_self.files.url)
        if os.path.isfile(settings.MEDIA_ROOT + '/' + old_self.files.name) and instance.files.closed:
            if settings.MEDIA_ROOT + '/' + old_self.files.name != settings.MEDIA_ROOT + '/' + names:
                os.replace(settings.MEDIA_ROOT + '/' + old_self.files.name, settings.MEDIA_ROOT + '/' + names)
                instance.files = names

        if old_self.files and old_self.files != instance.files:
            old_self.files.delete(False)

@receiver(pre_save, sender = Image_Storage)
def image_rename(sender, instance, **kwargs):
    if instance.pk is not None:
        old_self = sender.objects.get(pk=instance.pk)
        # если поменялось название и не изменился файл
        # if old_self.title_files and instance.title_files != old_self.title_files and old_self.files == instance.files or \
        #     instance.file_type != old_self.file_type and old_self.files == instance.files:
        names = upload_location_image(instance, old_self.image.url)
        if os.path.isfile(settings.MEDIA_ROOT + '/' + old_self.image.name) and instance.image.closed:
            if settings.MEDIA_ROOT + '/' + old_self.image.name != settings.MEDIA_ROOT + '/' + names:
                print('hello')
                print( settings.MEDIA_ROOT + '/' + old_self.image.name)
                print(settings.MEDIA_ROOT + '/' + names)
                os.replace(settings.MEDIA_ROOT + '/' + old_self.image.name, settings.MEDIA_ROOT + '/' + names)
                instance.image = names

        if old_self.image and old_self.image != instance.image:
            old_self.image.delete(False)

@receiver(post_delete, sender=Image_Storage)
def image_delete(sender, instance, **kwargs):
    if instance.image:
       print('delete images')
       instance.image.close()
       instance.image.delete(False)

@receiver(post_delete, sender=File_Storage)
def file_delete(sender, instance, **kwargs):
    if instance.files:
       instance.files.close()
       instance.files.delete(False)