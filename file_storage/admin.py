from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from file_storage.models import File_Storage, File_Type, Image_Storage
from django.utils.html import mark_safe

admin.site.site_title = "Файловое хранилище"
admin.site.site_header = "Файловое хранилище"

class File_StorageInline(GenericTabularInline):  #  Добавляем продукты к категориям в админке
    model = File_Storage
    extra = 0
    fields = ('files', 'title_files', 'file_type', 'date_files')
    readonly_fields = ('date_files',)
    view_on_site = False  # Ссылка смотреть на сайте get_absolute_url
    # can_delete = False  # можно ли удалять со страницы категорий товары
    # show_change_link = True  # ссылка на страницу редактирования товара
    max_num = 4
    # original = False
    # # ct_fk_field = "object_id"
    # # ct_field = "content_type"

class Image_StorageInline(GenericTabularInline):  #  Добавляем продукты к категориям в админке
    model = Image_Storage
    extra = 0
    fields = ('image', 'title_image', 'resize', 'get_image',)
    readonly_fields = ('get_image',)
    view_on_site = False  # Ссылка смотреть на сайте get_absolute_url
    # can_delete = False  # можно ли удалять со страницы категорий товары
    # show_change_link = True  # ссылка на страницу редактирования товара
    max_num = 4
    # original = False
    # # ct_fk_field = "object_id"
    # # ct_field = "content_type"
    def get_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src = {obj.image.url} width ="50" height ="50"')
        else:
            return mark_safe(f'<img src = "/media/noimg.jpg" width="50" height="50" ')

    get_image.short_description = "Изображение"

@admin.register(File_Storage) # регистрируем в админке приложение category
class File_Storage(admin.ModelAdmin):
    fields = ('files', 'title_files', 'content_type', 'object_id', 'content_object','file_type','date_files')
    readonly_fields = ('files', 'title_files', 'content_type', 'object_id', 'content_object', 'date_files')

@admin.register(Image_Storage) # регистрируем в админке приложение category
class Image_Storage(admin.ModelAdmin):
    fields = ('image', 'title_image', 'content_type', 'object_id', 'content_object', 'resize', 'get_image',)
    readonly_fields = ('image', 'title_image', 'content_type', 'object_id', 'content_object', 'get_image',)

    def get_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src = {obj.image.url} width ="50" height ="50"')
        else:
            return mark_safe(f'<img src = "/media/noimg.jpg" width="50" height="50" ')

    get_image.short_description = "Изображение"


@admin.register(File_Type) # регистрируем в админке приложение File_Type
class File_Type(admin.ModelAdmin):
    fields = ('name',)


