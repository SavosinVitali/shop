import sys
from django.db.models.signals import post_delete, pre_save, post_save
from django.dispatch.dispatcher import receiver
from file_storage.models import upload_location_image, upload_location_file, Image_Storage, File_Storage
import os
from django.conf import settings
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from shop.settings import SIZES_IMAGE, RESIZES_IMAGE
import magic


def image_name_generator(logo):
    """Функция генерирует имена файлов исходя из разрешений изображения"""
    name = []
    filebase, extension = logo.rsplit('.', maxsplit=1)
    name.append(settings.MEDIA_ROOT + '/' + logo)
    for size in SIZES_IMAGE:
        name.append(settings.MEDIA_ROOT + '/%s_%s.%s' % (filebase, size[0], extension))
    return name

def folder_del(folder):
    """ Удаляем папки в которых нет файлов"""
    for dir, subdirs, files in os.walk(folder):
        if subdirs == [] and files == []:
            try:
                os.rmdir(dir)
                print("Директория '%s' успешно удалена" % dir)
            except OSError as error:
                print(error)
                print("Директория '%s' не может быть удалена" % dir)
    try:
        if os.listdir(folder) == []:
            try:
                os.rmdir(folder)
                print("Директория '%s' успешно удалена" % folder)
            except OSError as error:
                print(error)
                print("Директория '%s' не может быть удалена" % folder)
    except OSError as error:
        print(error)
        print("Директории '%s' не существует" % folder)




"""Функция конвертирует делает миниатюры JPEG согласно SIZES_IMAGE в Settings """
@receiver(post_save, sender=Image_Storage)
def resize_image(sender, instance, **kwargs):
    if instance.pk is not None and instance.image and instance.resize:
        names = image_name_generator(instance.image.name)
        for name in names:
            try:
                im = Image.open(names[0])
            except OSError as error:
                print(error)
                print("Файл '%s' не существует" % names[0])
            else:
                if names.index(name) != 0:
                    if not os.path.isfile(name):
                        im.thumbnail(SIZES_IMAGE[names.index(name)-1])
                        print(name, 'Создана миниатюра')
                        im.save(name)

@receiver(pre_save, sender=File_Storage)
def file_rename(sender, instance, **kwargs):
    if instance.pk is not None:
        old_self = sender.objects.get(pk=instance.pk)
        names = upload_location_file(instance, old_self.files.url)
        if os.path.isfile(settings.MEDIA_ROOT + '/' + old_self.files.name) and instance.files.closed:
            if settings.MEDIA_ROOT + '/' + old_self.files.name != settings.MEDIA_ROOT + '/' + names:
                os.renames(settings.MEDIA_ROOT + '/' + old_self.files.name, settings.MEDIA_ROOT + '/' + names)
                instance.files = names

        if old_self.files and old_self.files != instance.files:
            old_self.files.close()
            old_self.files.delete(False)

@receiver(pre_save, sender=Image_Storage)
def image_rename(sender, instance, **kwargs):
    print('pree_save')
    if instance.pk is not None:
        old_self = sender.objects.get(pk=instance.pk)
        names = upload_location_image(instance, old_self.image.name)
        instance.image = names
        if os.path.isfile(settings.MEDIA_ROOT + '/' + old_self.image.name) and instance.image.closed:
            if old_self.image.name != names:
                if old_self.resize:
                    names_old = image_name_generator(old_self.image.name)
                    names_new = image_name_generator(names)
                    for name in names_old:
                        if os.path.isfile(name):
                            os.renames(name, names_new[names_old.index(name)])
                else:
                    os.renames(settings.MEDIA_ROOT + '/' + old_self.image.name, settings.MEDIA_ROOT + '/' + names)

            """если изменилось имя файла удаляем старые имена и папки"""
        # if old_self.image and old_self.image != instance.image:
        #     folder = names.rsplit('/', maxsplit=2)
        #     names = image_name_generator(instance.image.name)
        #     """ Удаляем файлы """
        #     for name in names:
        #         if os.path.isfile(name):
        #             print(name, 'удаляем файл')
        #             os.remove(name)
        #     folder_del(settings.MEDIA_ROOT + '/' + folder[0])

        if old_self.resize != instance.resize and not instance.resize:
            names = image_name_generator(instance.image.name)
            for name in names:
                if names.index(name) != 0:
                    if os.path.isfile(name):
                        print(name, 'удаляем файл')
                        os.remove(name)



"""Функция конвертирует загружаемые картинки в JPEG когда в админке выбираем новый файл"""
@receiver(pre_save, sender=Image_Storage)
def image_convert_jpeg(sender, instance, **kwargs):
    if instance.image.closed is False:
        content_type = magic.from_buffer(instance.image.read(1024), mime=True)
        if content_type == 'image/jpeg':
            new_img = Image.open(instance.image).convert('RGB')
            new_img.thumbnail(RESIZES_IMAGE, Image.ANTIALIAS)
            output = BytesIO()
            new_img.save(output, 'JPEG', quality=80)
            output.seek(0)
            instance.image = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % instance.image.name, 'image/jpeg',
                                              sys.getsizeof(output), None)


        if content_type == 'image/x-ms-bmp':
            new_img = Image.open(instance.image).convert('RGB')
            new_img.thumbnail(RESIZES_IMAGE, Image.ANTIALIAS)
            output = BytesIO()
            new_img.save(output, 'JPEG', quality=80)
            output.seek(0)
            instance.image = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % instance.image.name, 'image/jpeg',
                                              sys.getsizeof(output), None)


        if content_type == 'image/png':
            png = Image.open(instance.image).convert('RGBA')
            background = Image.new("RGBA", png.size, (255, 255, 255))
            alpha_composite = Image.alpha_composite(background, png).convert('RGB')
            alpha_composite.thumbnail(RESIZES_IMAGE, Image.ANTIALIAS)
            output = BytesIO()
            alpha_composite.save(output, 'JPEG', quality=80)
            output.seek(0)
            instance.image = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % instance.image.name, 'image/jpeg',
                                              sys.getsizeof(output), None)



@receiver(post_delete, sender=Image_Storage)
def image_delete(sender, instance, **kwargs):
    if instance.image:
        names = image_name_generator(instance.image.name)
        folder = names[0].rsplit('/', maxsplit=2)
        for name in names:
            if os.path.isfile(name):
               os.remove(name)
        folder_del(folder[0])
       # instance.image.close()
       # instance.image.delete(False)

@receiver(post_delete, sender=File_Storage)
def file_delete(sender, instance, **kwargs):
    if instance.files:
       folder = instance.files.name.rsplit('/', maxsplit=2)

       if os.path.isfile(settings.MEDIA_ROOT + '/' + instance.files.name):
           os.remove(settings.MEDIA_ROOT + '/' + instance.files.name)
       folder_del(settings.MEDIA_ROOT + '/' + folder[0])
