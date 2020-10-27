from django.core.exceptions import ValidationError
from django.template.defaultfilters import filesizeformat
import magic
from django.utils.deconstruct import deconstructible

@deconstructible
class FileValidator(object):
    error_messages = {
     'no_file': "Файл удален выберите другой файл либо очиститe",
     'max_size': "Вы привысили максимальный размер файла %(max_size), Размер вашего файла %(size)",
     'min_size': "Ensure this file size is not less than %(min_size)s. "
                  "Your file size is %(size)s.",
     'content_type': "Files of type %(content_type)s are not supported.",
    }

    def __init__(self, max_size=None, min_size=None, content_types=()):
        self.max_size = max_size
        self.min_size = min_size
        self.content_types = content_types

    def __call__(self, data):
        # проверяем не удалили файл
        print('validator')
        try:
            data.size
        except:
            raise ValidationError(self.error_messages['no_file'])
        # проверяем максимальный размер файла
        if self.max_size is not None and data.size > self.max_size:
            params = {
                'max_size': filesizeformat(self.max_size),
                'size': filesizeformat(data.size),
            }
            raise ValidationError(self.error_messages['max_size'], 'max_size', params)
        if self.min_size is not None and data.size < self.min_size:
            params = {
                'min_size': filesizeformat(self.min_size),
                'size': filesizeformat(data.size)
            }
            raise ValidationError(self.error_messages['min_size'], 'min_size', params)
        if self.content_types:
            temp_file = data.read(2048)
            content_type = magic.from_buffer(temp_file, mime=True)
            if content_type not in self.content_types:
                params = {'content_type': content_type}
                raise ValidationError(self.error_messages['content_type'], "content_type", params)

    def __eq__(self, other):
        return isinstance(other, FileValidator)