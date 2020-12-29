import sys

from django.db.models.signals import post_delete, pre_save, post_save
from django.dispatch.dispatcher import receiver
from file_storage.models import File_Storage, upload_location_file, Image_Storage, upload_location_image
import os
from django.conf import settings
from PIL import Image
from io import StringIO, BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from pytils.translit import slugify

# def file_name_generator(logo):
#     """Функция генерирует имена файлов исходя из разрешений изображения"""
#     name = []
#     filebase, extension = logo.split('.')
#     name.append(settings.MEDIA_ROOT + '/' + logo)
#     for size in SIZES_IMAGE:
#         name.append(settings.MEDIA_ROOT + '/%s_%s.%s' % (filebase, size[0], extension))
#     return name


# @receiver(post_save, sender=Product)
# def file_storage_resave_product(sender, instance, **kwargs):
#     if instance.pk is not None:
#         for name in instance.files.all():
#             name.files.close()
#             name.save()
# def resize_image(sender, instance, **kwargs):
#     if instance.pk is not None and instance.logo:
#         names = file_name_generator(instance.logo.name)
#         for name in names:
#             im = Image.open(names[0])
#             if names.index(name) != 0:
#                 im.thumbnail(SIZES_IMAGE[names.index(name)-1])
#             im.save(name)



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
                os.renames(settings.MEDIA_ROOT + '/' + old_self.files.name, settings.MEDIA_ROOT + '/' + names)
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
                os.renames(settings.MEDIA_ROOT + '/' + old_self.image.name, settings.MEDIA_ROOT + '/' + names)
                instance.image = names

        if instance.image.closed is False:
            print('otkrita kartina')
            image = instance.image
            img = Image.open(image)
            new_img = img.convert('RGB')
            new_img.thumbnail((600,600), Image.ANTIALIAS)
            output = BytesIO()
            new_img.save(output, 'JPEG', quality=90)
            output.seek(0)
            instance.image = InMemoryUploadedFile(output,'ImageField', "%s.jpg" %instance.image.name, 'image/jpeg', sys.getsizeof(output), None)

        if old_self.image and old_self.image != instance.image:
            old_self.image.delete(False)

@receiver(post_delete, sender=Image_Storage)
def image_delete(sender, instance, **kwargs):
    if instance.image:
       instance.image.close()
       instance.image.delete(False)

@receiver(post_delete, sender=File_Storage)
def file_delete(sender, instance, **kwargs):
    if instance.files:
       instance.files.close()
       instance.files.delete(False)


# image = Img.open(StringIO.StringIO(self.photo.read()))
#             image.thumbnail((200,200), Img.ANTIALIAS)
#             output = StringIO.StringIO()
#             image.save(output, format='JPEG', quality=75)
#             output.seek(0)
#             self.photo= InMemoryUploadedFile(output,'ImageField', "%s.jpg" %self.photo.name, 'image/jpeg', output.len, None)