from django.core.exceptions import ValidationError
from django.template.defaultfilters import filesizeformat
import magic
from django.utils.deconstruct import deconstructible
from django.conf import settings


@deconstructible
class FileValidator(object):
    error_messages = {
     'no_file': "Файл удален выберите другой файл либо очиститe",
     'file_ready': "Файл занят",
     'max_size': "Вы привысили максимальный размер файла %(max_size)s, Размер вашего файла %(size)s",
     'min_size': "Минимальный размер загружаемого файла %(min_size)s, Размер вашего файла %(size)s",
     'content_type': "Тип загружаемого файла %(content_type)s. Загрузиет %(old_content_type)s",
    }

    def __init__(self, max_size=None, min_size=None, content_types=()):
        self.max_size = max_size
        self.min_size = min_size
        self.content_types = content_types


    def __call__(self, data):
        # проверяем не удалили файл
        try:
            data.size
        except:
            raise ValidationError(self.error_messages['no_file'])
        # проверяем разрешение файла
        if self.content_types:
            print('Validator')
            content_type = magic.from_buffer(data.read(1024), mime=True)
            if content_type not in self.content_types:
                     params = {'content_type': content_type,
                                      'old_content_type': self.content_types}
                     raise ValidationError(self.error_messages['content_type'], "content_type", params)
        # проверяем максимальный размер файла
        if self.max_size is not None and data.size > self.max_size:
            params = {
                'max_size': filesizeformat(self.max_size),
                'size': filesizeformat(data.size),
            }
            raise ValidationError(self.error_messages['max_size'], 'max_size', params)
        # проверяем минимальный размер файла
        if self.min_size is not None and data.size < self.min_size:
            params = {
                'min_size': filesizeformat(self.min_size),
                'size': filesizeformat(data.size)
            }
            raise ValidationError(self.error_messages['min_size'], 'min_size', params)

    def __eq__(self, other):
        return isinstance(other, FileValidator)