import os
import sys
from django.contrib.contenttypes.fields import GenericForeignKey
from PIL import Image
from pytils.translit import slugify
from django.db import models
from django.conf import settings
from shop.settings import SIZES_IMAGE, RESIZES_IMAGE, SIZE_DOWNLOAD_IMAGE
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib.contenttypes.models import ContentType
import magic
from file_storage.validations import FileValidator


def upload_location_file(instance, filename):
    filebase, extension = filename.rsplit('.', maxsplit=1)
    classen = instance.content_object.__class__.__name__
    return 'file_storage/%s/%s/files/%s_%s_%s.%s' % (slugify(instance.content_object.__class__.__name__),
                                                     slugify(instance.content_object),
                                                     slugify(instance.title_files),
                                                     slugify(instance.content_object),
                                                     slugify(instance.file_type),
                                                     extension)

def upload_location_image(instance, filename):
    filebase, extension = filename.rsplit('.', maxsplit=1)
    return 'file_storage/%s/%s/images/%s.%s' % (slugify(instance.content_object.__class__.__name__),
                                                   slugify(instance.content_object),
                                                   slugify(instance.content_object),
                                                   extension)

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


    def __init__(self, *args, **kwargs):
        super(File_Storage, self).__init__(*args, **kwargs)
        self._old_files = self.files
        self._old_title_files = self.title_files


    def files_renames(self, *args, **kwargs):
        self.files = upload_location_file(self, self.files.name)
        return self.files



    def files_renames_os(self, *args, **kwargs):
        if os.path.isfile(settings.MEDIA_ROOT + '/' + self._old_files.name):
            os.renames(settings.MEDIA_ROOT + '/' + self._old_files.name, settings.MEDIA_ROOT + '/' + self.files.name)

    """Функция удаляет файлы на жестком диске"""
    def delete_files(self, *args, **kwargs):
        if os.path.isfile(settings.MEDIA_ROOT + '/' + self._old_files.name):
            os.remove(settings.MEDIA_ROOT + '/' + self._old_files.name)

    """ Удаляем папки в которых нет файлов"""
    def folder_del(self, *args, **kwargs):
        folder = self._old_files.name.rsplit('/', maxsplit=2)
        folder = settings.MEDIA_ROOT + '/' + folder[0]
        for dir, subdirs, files in os.walk(folder):
            if subdirs == [] and files == []:
                try:
                    os.rmdir(dir)
                except OSError as error:
                    print(error)
                    print("Директория '%s' не может быть удалена" % dir)
        try:
            if os.listdir(folder) == []:
                try:
                    os.rmdir(folder)
                except OSError as error:
                    print(error)
                    print("Директория '%s' не может быть удалена" % folder)
        except OSError as error:
            print(error)
            print("Директории '%s' не существует" % folder)


class Image_Storage(models.Model):
    image = models.ImageField(upload_to=upload_location_image, blank=False, null=False, verbose_name='Изображение',
                              help_text="Загрузите изображение не мение 1920x1080",
                              validators=[FileValidator(max_size=1024 * 1024 * 5.1,
                                                        content_types=('image/jpeg', 'image/png', 'image/x-ms-bmp'),
                                                        min_resolution = SIZE_DOWNLOAD_IMAGE)])
    title_image = models.CharField(max_length=200,  verbose_name="Описание изображения (Title)", blank=True)
    alt_image = models.CharField(max_length=200,  verbose_name="Описание изображения (Alt)", blank=True)
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
        self._old_resize = self.resize


    def image_renames(self, *args, **kwargs):
        self.image = upload_location_image(self, self.image.name)
        return self.image

    def alt_image_generator(self, *args, **kwargs):
        self.alt_image = '%s' % (self.content_object)
        return self.alt_image

    def title_image_generator(self, *args, **kwargs):
        self.title_image = '%s. Фирма: %s Cтрана производства: %s' % (self.content_object,
                                                                   self.content_object.brand,
                                                                   self.content_object.brand.country.name)
        return self.title_image

    """Функция создает миниатюры на жестком диске"""
    def create_resize_image(self, *args, **kwargs):
        print('create resize image')
        names = image_name_generator(self.image.name)
        for name in names:
            try:
                im = Image.open(names[0])
            except OSError as error:
                print(error)
                print("Файл '%s' не существует" % names[0])
            else:
                if names.index(name) != 0:
                    if not os.path.isfile(name):
                        im.thumbnail(SIZES_IMAGE[names.index(name) - 1])
                        im.save(name)

    """Функция удаляет файлы на жестком диске"""
    def delete_image(self, *args, **kwargs):
        if self._old_resize:
            names = image_name_generator(self._old_image.name)
            for name in names:
                if os.path.isfile(name):
                    os.remove(name)
        else:
            if os.path.isfile(settings.MEDIA_ROOT + '/' + self._old_image.name):
                os.remove(settings.MEDIA_ROOT + '/' + self._old_image.name)

    """Функция удаляет миниатюры на жестком диске"""
    def delete_resize_image(self, *args, **kwargs):
        names = image_name_generator(self.image.name)
        print(names, 'delete resize image')
        for name in names:
            if names.index(name) != 0:
                if os.path.isfile(name):
                    os.remove(name)


    """Функция переименовывает файлы на жестком диске"""
    def image_renames_os(self, *args, **kwargs):
        if self._old_resize and self.resize:
            names_new = image_name_generator(self.image.name)
            names_old = image_name_generator(self._old_image.name)
            for name in names_old:
                if os.path.isfile(name):
                    os.renames(name, names_new[names_old.index(name)])
        else:
            if os.path.isfile(settings.MEDIA_ROOT + '/' + self._old_image.name):
                os.renames(settings.MEDIA_ROOT + '/' + self._old_image.name, settings.MEDIA_ROOT + '/' + self.image.name)


    """Функция конвертирует загружаемые картинки в JPEG когда в админке выбираем новый файл"""
    def image_convert_jpeg(self, *args, **kwargs):
        content_type = magic.from_buffer(self.image.read(1024), mime=True)
        if content_type == 'image/jpeg':
            new_img = Image.open(self.image).convert('RGB')
            new_img.thumbnail(RESIZES_IMAGE, Image.ANTIALIAS)
            output = BytesIO()
            new_img.save(output, 'JPEG', quality=80)
            output.seek(0)
            self.image = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % self.image.name,
                                              'image/jpeg', sys.getsizeof(output), None)

        if content_type == 'image/x-ms-bmp':
            new_img = Image.open(self.image).convert('RGB')
            new_img.thumbnail(RESIZES_IMAGE, Image.ANTIALIAS)
            output = BytesIO()
            new_img.save(output, 'JPEG', quality=80)
            output.seek(0)
            self.image = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % self.image.name,
                                              'image/jpeg', sys.getsizeof(output), None)

        if content_type == 'image/png':
            png = Image.open(self.image).convert('RGBA')
            background = Image.new("RGBA", png.size, (255, 255, 255))
            alpha_composite = Image.alpha_composite(background, png).convert('RGB')
            alpha_composite.thumbnail(RESIZES_IMAGE, Image.ANTIALIAS)
            output = BytesIO()
            alpha_composite.save(output, 'JPEG', quality=80)
            output.seek(0)
            self.image = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % self.image.name,
                                              'image/jpeg', sys.getsizeof(output), None)

    def folder_del(self, *args, **kwargs):
        """ Удаляем папки в которых нет файлов"""
        folder = self._old_image.name.rsplit('/', maxsplit=2)
        folder = settings.MEDIA_ROOT + '/' + folder[0]
        for dir, subdirs, files in os.walk(folder):
            if subdirs == [] and files == []:
                try:
                    os.rmdir(dir)
                except OSError as error:
                    print(error)
                    print("Директория '%s' не может быть удалена" % dir)
        try:
            if os.listdir(folder) == []:
                try:
                    os.rmdir(folder)
                except OSError as error:
                    print(error)
                    print("Директория '%s' не может быть удалена" % folder)
        except OSError as error:
            print(error)
            print("Директории '%s' не существует" % folder)