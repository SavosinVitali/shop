from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from pytils.translit import slugify

from django.contrib.contenttypes.models import ContentType

from file_storage.validations import FileValidator


def upload_location_file(instance, filename):
    filebase, extension = filename.rsplit('.', maxsplit=1)
    original = File_Storage.objects.filter(object_id=instance.object_id).count()
    return 'file_storage/%s/%s_%s.%s' % (slugify(instance.content_object.__class__.__name__), slugify(instance.content_object),original, extension)

class File_Storage(models.Model):

    files = models.FileField(upload_to=upload_location_file,
                             blank=False, verbose_name="Имя файла",
                           validators=[FileValidator(max_size=1024 * 1024 * 5.1, content_types=('application/pdf',))])
    title_files = models.CharField(max_length=200, db_index=True, verbose_name="Описание файла", null=True, blank=False)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name="К чему относится файл")
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        verbose_name = 'Хранилище файла'
        verbose_name_plural = "Хранилище файлов"

    def __str__(self):
        return self.title_files
