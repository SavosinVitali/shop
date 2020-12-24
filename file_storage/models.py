from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from pytils.translit import slugify

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