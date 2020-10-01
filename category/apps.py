from django.apps import AppConfig


class CategoryConfig(AppConfig):
    name = 'category'
    verbose_name = "Категории"

    def ready(self):
        from category import signals