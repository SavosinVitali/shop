from django.apps import AppConfig


class FileStorageConfig(AppConfig):
    name = 'file_storage'
    verbose_name = "Файловое хранилище"

    def ready(self):
        from file_storage import signals