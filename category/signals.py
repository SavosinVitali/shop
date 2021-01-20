from typing import List, Tuple

from django.core.exceptions import ValidationError
from django.db.models.signals import post_delete, pre_save, post_save
from django.dispatch.dispatcher import receiver
from category.models import Brand, Product ,upload_location_image, File_Storage, Image_Storage
from pytils.translit import slugify
import os
from django.conf import settings
from PIL import Image
from sorl.thumbnail import get_thumbnail

# from shop.settings import SIZES_IMAGE
# from file_storage.signals import file_rename_1


# def file_name_generator(logo):
#     """Функция генерирует имена файлов исходя из разрешений изображения"""
#     name = []
#     filebase, extension = logo.split('.')
#     name.append(settings.MEDIA_ROOT + '/' + logo)
#     for size in SIZES_IMAGE:
#         name.append(settings.MEDIA_ROOT + '/%s_%s.%s' % (filebase, size[0], extension))
#     return name


# @receiver(post_delete, sender=Brand)
# def logo_delete(sender, instance, **kwargs):
#     if instance.logo.name:
#        print('post_delete')
#        instance.logo.delete(False)
#     if instance.iso.name:
#        instance.iso.delete(False)

# @receiver(pre_save, sender=Brand)
# def logo_add(sender, instance, **kwargs):
#     if instance.pk is not None:
#        old_self = sender.objects.get(pk=instance.pk)
#        if old_self.logo and instance.logo != old_self.logo:
#            names = file_name_generator(old_self.logo.name)
#            for name in names:
#                if os.path.isfile(name):
#                   os.remove(name)
#         # """Если произошло изменение имени удаляем ISO"""
#        if old_self.iso and instance.iso != old_self.iso:
#           old_self.iso.delete(False)
#         # """Если произошло изменение имени меняем название изображений"""
#        if instance.name != old_self.name and os.path.isfile(settings.MEDIA_ROOT + '/' + instance.logo.name):
#            new_path = upload_location_image(instance, instance.logo.name)
#            names_old = file_name_generator(old_self.logo.name)
#            names = file_name_generator(new_path)
#            instance.logo.close()
#            for name in names:
#               if os.path.isfile(names_old[names.index(name)]):
#                  os.rename(names_old[names.index(name)], name)
#            instance.logo = new_path

"""Делаем уменьшеные копии изображения name_SIZES_IMAGE из settings """
@receiver(post_save, sender=Product)
@receiver(post_save, sender=Brand)
def file_storage_resave_files(sender, instance, **kwargs):
    if instance.pk is not None and instance.name != instance._old_name:
        for name in instance.files.all():
            name.save(update_fields=['files'])

@receiver(post_save, sender=Product)
def file_storage_resave_image(sender, instance, **kwargs):
    print(instance.name, instance._old_name, 'Dannie produkta')
    if instance.pk is not None and instance.name != instance._old_name:
        for name in instance.image.all():
            name.save(update_fields=['image', 'alt_image', 'title_image'])
            print('Sohranenie produkta')

@receiver(post_save, sender=Brand)
def file_storage_resave_image2(sender, instance, **kwargs):
    if instance.pk is not None:
        if instance.name != instance._old_name or instance._old_country != instance.country:
            for product in Product.objects.filter(brand_id=instance.pk):
                for name in product.image.all():
                    name.save(update_fields=['image', 'alt_image', 'title_image'])
                    print('Sohranenie produkta')
            print('brend izmenilsa')

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

# @receiver(pre_save, sender = File_Storage)
# def logo_add(sender, instance, **kwargs):
#     # print('instance')
#     # print(instance)
#     pass
#     # if instance.pk is not None:
#     #    old_self = sender.objects.get(pk=instance.pk)
#     #    if old_self.logo and instance.logo != old_self.logo:
#     #        names = file_name_generator(old_self.logo.name)
#     #        for name in names:
#     #            if os.path.isfile(name):
#     #               os.remove(name)
#     #     # """Если произошло изменение имени удаляем ISO"""
#     #    if old_self.iso and instance.iso != old_self.iso:
#     #       old_self.iso.delete(False)
#     #     # """Если произошло изменение имени меняем название изображений"""
#     #    if instance.name != old_self.name and os.path.isfile(settings.MEDIA_ROOT + '/' + instance.logo.name):
#     #        new_path = upload_location_image(instance, instance.logo.name)
#     #        names_old = file_name_generator(old_self.logo.name)
#     #        names = file_name_generator(new_path)
#     #        instance.logo.close()
#     #        for name in names:
#     #           if os.path.isfile(names_old[names.index(name)]):
#     #              os.rename(names_old[names.index(name)], name)
#     #        instance.logo = new_path