from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from mptt.admin import TreeRelatedFieldListFilter
from sorl.thumbnail import get_thumbnail

from category.models import Category, Product, ProductImage, Attributes, Brand
from file_storage.admin import File_StorageInline
from file_storage.models import File_Storage
from mptt.admin import MPTTModelAdmin
from django.utils.html import format_html, mark_safe
from django.forms.models import BaseModelFormSet, BaseInlineFormSet


# Register your models here.
from django.forms import formset_factory
from sorl.thumbnail.admin import AdminImageMixin
from django.utils import timezone
from django.contrib.postgres import fields
from django.contrib.postgres.fields import JSONField

from .forms import CategoryAdminForm, ProductAdminForm, BrandAdminForm
from django.contrib.contenttypes.admin import GenericTabularInline

admin.site.site_title = "Админка магазина"
admin.site.site_header = "Админка магазина"

@admin.register(Brand) # регистрируем в админке приложение category
class BrandAdmin(admin.ModelAdmin):
    fields = ('name', 'history', 'country', ('iso', 'data_end_iso'), ('logo', 'get_logo'),)
    list_display = ('name', 'country', 'get_logo', 'data_end_iso')
    readonly_fields = ('get_logo',)
    inlines = (File_StorageInline,)  # Добавляем продукты к категориям в админ
    form = BrandAdminForm

    def get_logo(self, obj):
        if obj.logo:
            return mark_safe(f'<img src = {obj.logo.url} width="50" height="50" ')
        else:
            return mark_safe(f'<img src ="/media/noimg.jpg" width="50" height="50" ')

    get_logo.short_description = "Текущее изображение Брэнда"






class ProductImageInline(AdminImageMixin, admin.TabularInline):  #  Добавляем продукты к категориям в админке
    model = ProductImage
    extra = 0
    fields = ('get_image', 'image', 'title_image', )

    readonly_fields = ('get_image', ) #  поля которые не редактируются
    # view_on_site = False # Ссылка смотреть на сайте get_absolute_url
    # can_delete  = False #   можно ли удалять со страницы категорий товары
    # show_change_link = True #ссылка на страницу редактирования товара
    # max_num = 10
    # original = False

    def get_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src = {obj.image.url} width ="100" height ="100"' )
        else:
            return mark_safe(f'<img src = "/media/noimg.jpg" width="100" height="100" ' )


    get_image.short_description = "Изображение Товаров"


    # def has_add_permission(self, *args, **kwargs): #запрет на добавление нового объекта продуктов в категориях
    #       return False
    # def has_change_permission(request, obj):
    #     return True
    # list_display = ('name','available') # задаем какие поля в админке будут отображаться
    #fields = ('name', 'slug_home', 'description')



# class CategoryAdminForm(ModelForm):
#     class Meta:
#         model = Category
#         fields = '__all__'
#         widgets = {
#             'attributes': JSONEditorWidget(dynamic_schema, True)
#         }
#
#     class Media:
#         css = { "all" : ("css/admin_atributes.css",) }

    # def clean(self):
    #     super().clean()
    #     name = self.cleaned_data['attributes']
    #     print('hello')
    #     print(name)

@admin.register(Attributes) # регистрируем в админке приложение category
class AttributesAdmin(admin.ModelAdmin):
    pass

class AttributesInline(admin.TabularInline):  #  Добавляем продукты к категориям в админке
    model = Attributes
    extra = 0
    fields = ('name', 'description', 'available')
    # readonly_fields = ('name', 'description') #  поля которые не редактируются
    can_delete  = False #   можно ли удалять со страницы категорий товары
    show_change_link = True #ссылка на страницу редактирования товара
    max_num = 10

class ProductInlineFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super(ProductInlineFormSet, self).__init__(*args, **kwargs)



class ProductInline(AdminImageMixin, admin.TabularInline):  #  Добавляем продукты к категориям в админке
    model = Product
    extra = 0
    fields = ('name', 'description', 'available')
    readonly_fields = ('name', 'description') #  поля которые не редактируются
    view_on_site = False # Ссылка смотреть на сайте get_absolute_url
    can_delete  = False #   можно ли удалять со страницы категорий товары
    show_change_link = True #ссылка на страницу редактирования товара
    max_num = 10
    original = False
    formset = ProductInlineFormSet



    def has_add_permission(self, *args, **kwargs): #запрет на добавление нового объекта продуктов в категориях
          return False
    # def has_change_permission(request, obj):
    #     return True
    # list_display = ('name','available') # задаем какие поля в админке будут отображаться
    #fields = ('name', 'slug_home', 'description')

@admin.register(Category)
class CategoryAdmin(AdminImageMixin, DraggableMPTTAdmin):
    mptt_indent_field = "name"
    list_display = ('tree_actions', 'indented_title', 'slug', 'available', 'get_image',)
    list_display_links = ('indented_title',)
    prepopulated_fields = {'slug': ('name',)}# поле slug заполняется из поля name
    inlines = (ProductInline, AttributesInline,)  #  Добавляем продукты к категориям в админ
    # save_on_top = True # Кнопки сверху и снизу
    list_editable = ('available',)
    readonly_fields = ('get_image',)
    fields = ('name', 'parent' , 'slug' , ('image','get_image') )
    form = CategoryAdminForm


    class Media:
        css = { "all" : ("css/hide_admin_original.css",) }

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

    def get_image(self, obj):
         if obj.image:
            return mark_safe(f'<img src = {obj.image.url} width="50" height="50" ' )
         else:
            return mark_safe(f'<img src = "/media/noimg.jpg" width="50" height="50" ' )

    get_image.short_description = "Изображение Категории"










@admin.register(Product) # регистрируем в админке приложение category
class ProductAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = ('name', 'type_product', 'category' , 'slug' , 'slug_home', 'stock', 'available', 'created', 'get_image', ) # задаем какие поля в админке будут отображаться
    fields = ('category','type_product', ('name','available') , ('slug', 'slug_home'), ('stock','price'), ('created', 'updated'), )
    prepopulated_fields = {'slug': ('name',)}# поле slug заполняется из поля name
    raw_id_fields = ('category' ,) # добавляет поиск при создании данного поля
    list_editable = ('available','stock')
    readonly_fields = ('slug_home', 'created', 'updated') #  поля которые не редактируются
    inlines = (File_StorageInline,)  #  Добавляем продукты к категориям в админ
    form = ProductAdminForm

    def get_image(self, obj):
        if obj.productimage_set.all()[:1].get().image:
            return mark_safe(f'<img src ={obj.productimage_set.all()[:1].get().image.url} width="50" height="50">' )
        else:
            return mark_safe(f'<img src = "/media/noimg.jpg" width="50" height="50" ' )

    get_image.short_description = "Изображение Товара"
