from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from file_storage.models import File_Storage, File_Type


admin.site.site_title = "Файловое хранилище"
admin.site.site_header = "Файловое хранилище"

class File_StorageInline(GenericTabularInline):  #  Добавляем продукты к категориям в админке
    model = File_Storage
    extra = 0
    # view_on_site = False  # Ссылка смотреть на сайте get_absolute_url
    # can_delete = False  # можно ли удалять со страницы категорий товары
    # show_change_link = True  # ссылка на страницу редактирования товара
    max_num = 4
    # original = False
    # # ct_fk_field = "object_id"
    # # ct_field = "content_type"

@admin.register(File_Storage) # регистрируем в админке приложение category
class File_Storage(admin.ModelAdmin):
    fields = ('files', 'title_files', 'content_type', 'object_id', 'content_object','file_type',)
    readonly_fields = ('files', 'title_files', 'content_type', 'object_id', 'content_object')


@admin.register(File_Type) # регистрируем в админке приложение category
class File_Type(admin.ModelAdmin):
    fields = ('name',)


