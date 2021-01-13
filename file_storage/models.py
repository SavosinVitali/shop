import os

from django.contrib.contenttypes.fields import GenericForeignKey

from pytils.translit import slugify
from django.db import models
from django.conf import settings
from shop.settings import SIZES_IMAGE, RESIZES_IMAGE


from django.contrib.contenttypes.models import ContentType

from file_storage.validations import FileValidator


def upload_location_file(instance, filename):
    filebase, extension = filename.rsplit('.', maxsplit=1)
    classen = instance.content_object.__class__.__name__
    return 'file_storage/%s/%s/files/%s_%s_%s.%s' % (slugify(instance.content_object.__class__.__name__),  slugify(instance.content_object), slugify(instance.title_files),
                                                   slugify(instance.content_object), slugify(instance.file_type), extension)

def upload_location_image(instance, filename):
    filebase, extension = filename.rsplit('.', maxsplit=1)
    classen = instance.content_object.__class__.__name__
    return 'file_storage/%s/%s/images/%s_%s.%s' % (slugify(instance.content_object.__class__.__name__), slugify(instance.content_object), slugify(instance.title_image),
                                            slugify(instance.content_object), extension)

def image_name_generator(logo):
    """Функция генерирует имена файлов исходя из разрешений изображения"""
    name = []
    filebase, extension = logo.rsplit('.', maxsplit=1)
    name.append(settings.MEDIA_ROOT + '/' + logo)
    for size in SIZES_IMAGE:
        name.append(settings.MEDIA_ROOT + '/%s_%s.%s' % (filebase, size[0], extension))
    return name

class File_Type(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name="Название типа файла")

    class Meta:
        verbose_name = 'Тип файла'
        verbose_name_plural = 'Тип файлов'
        ordering = ['name']

    def __str__(self):
        return self.name


class File_Storage(models.Model):

    files = models.FileField(upload_to=upload_location_file,
                             blank=False, verbose_name="Имя файла",
                           validators=[FileValidator(max_size=1024 * 1024 * 5.1, content_types=('application/pdf',))])
    title_files = models.CharField(max_length=200, verbose_name="Название файла", null=True, blank=False, unique = True)
    date_files = models.DateField(auto_now=True, verbose_name='Дата')
    file_type = models.ForeignKey(File_Type, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Тип файла")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name="К чему относится файл")
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = "Файлы"

    def __str__(self):
        return self.title_files

class Image_Storage(models.Model):
    image = models.ImageField(upload_to=upload_location_image, blank=True, null=True, verbose_name='Изображение',
                              help_text="Загрузите изображение не мение 1920x1080",
                              validators=[FileValidator(max_size=1024 * 1024 * 5.1,
                                                        content_types=('image/jpeg', 'image/png', 'image/x-ms-bmp'),
                                                        min_resolution =(1920, 1080))])
    title_image = models.CharField(max_length=200, db_index=True, verbose_name="Описание изображения", null=True, blank=False)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name="К чему относится файл")
    resize = models.BooleanField(default=True, verbose_name="Делать миниатюры изображений")
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'

    def __str__(self):
        return self.title_image

    def __init__(self, *args, **kwargs):
        super(Image_Storage, self).__init__(*args, **kwargs)
        self._old_image = self.image
        self._old_title_image = self.title_image

    def has_changed(self):
        for field in self.__important_fields:
            print('---------change---------------', field)
            orig = '__original_%s' % field
            if getattr(self, orig) != getattr(self, field):
                return True
        return False

    def save(self,  *args, **kwargs):
        # Prep the data
        print('izmenenie')
        super(Image_Storage, self).save(*args, **kwargs)
            # If we're down with commitment, save this shit



    def image_renames(self, *args, **kwargs):
        self.image = upload_location_image(self, self.image.name)
        return self.image

    def image_renames_os(self, resize = False, *args, **kwargs):
        names_old = image_name_generator(self._old_image.name)
        names_new = image_name_generator(self.image.name)
        for name in names_old:
            if os.path.isfile(name):
                os.renames(name, names_new[names_old.index(name)])
        # if os.path.isfile(settings.MEDIA_ROOT + '/' + self._old_image.name):
        #     os.renames(settings.MEDIA_ROOT + '/' + self._old_image.name, settings.MEDIA_ROOT + '/' + self.image.name)


            # old_self = self.objects.get(pk=instance.pk)
            # if self.image.name != upload_location_image(self, self.image.name):
            #     self.image = upload_location_image(self, self.image.name)
            #     print('save models')


            # instance.image = names
            # if os.path.isfile(settings.MEDIA_ROOT + '/' + old_self.image.name) and instance.image.closed:
            #     if old_self.image.name != names:
            #         if old_self.resize:
            #             names_old = image_name_generator(old_self.image.name)
            #             names_new = image_name_generator(names)
            #             for name in names_old:
            #                 if os.path.isfile(name):
            #                     os.renames(name, names_new[names_old.index(name)])
            #         else:
            #             os.renames(settings.MEDIA_ROOT + '/' + old_self.image.name, settings.MEDIA_ROOT + '/' + names)