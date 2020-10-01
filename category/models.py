from django.db import models
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey
from sorl.thumbnail import ImageField
from django.contrib.postgres.fields import JSONField
from pytils.translit import slugify
from django_countries.fields import CountryField






def upload_location_brandimage(instance, filename):
    print(instance)
    filebase, extension = filename.split('.')
    return 'brand_img/%s.%s' % (slugify(instance.name), extension)

def upload_location_brandfile(instance, filename):
    filebase, extension = filename.split('.')
    return 'brand_iso/%s.%s' % (slugify(instance.name), extension)

class Brand(models.Model):
    """Класс брендов"""
    name = models.CharField(blank=True, max_length=100, verbose_name="Название Бренда")
    history = models.TextField(blank=True, max_length=400, verbose_name="История Бренда")
    country = CountryField(blank=True, default='CN', verbose_name="Страна происхождения")
    iso = models.FileField(upload_to=upload_location_brandfile, blank=True, verbose_name="Загрузите ISO Бренда")
    logo = models.ImageField(blank=True, upload_to=upload_location_brandimage, verbose_name="Изображение Бренда")

    class Meta:
        verbose_name = "Бренд"
        verbose_name_plural = "Бренды"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.pk is not None:
            old_self = Brand.objects.get(pk=self.pk)
            if old_self.logo and self.logo != old_self.logo:
               old_self.logo.delete(False)
            if old_self.iso and self.iso != old_self.iso:
               old_self.iso.delete(False)
        return super(Brand, self).save(*args, **kwargs)


class StatusManager(models.Manager):
    def get_queryset(self):
        return super(StatusManager, self).get_queryset().filter(available = True) # переопределение менеджера модели

def upload_location_categoryimage(instance, filename):
    filebase, extension = filename.split('.')
    return 'category_img/%s.%s' % (instance.slug, extension)

class Category(MPTTModel):
    name = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    slug = models.SlugField(max_length=200, unique = True)
    available = models.BooleanField(default=True, verbose_name="Доступен")
    image = models.ImageField(upload_to=upload_location_categoryimage, blank=True, null=True, verbose_name="Изображение категории")
    # attributes = JSONField(verbose_name="Атрибуты")
    # data = models.DateTimeField(auto_now_add=False, default = '2012-09-04 06:00:00.000000-08:00',verbose_name="дата")
    # data1 = models.DateField(auto_now_add=False, default = '2013-09-04',verbose_name="дата1")


    class MPTTMeta:
        order_insertion_by = ['parent_id']

    class Meta:
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'
        unique_together = ('slug', 'parent')
        #ordering = ['id']



    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category:product_list', kwargs={'path': self.get_path()})

    def save(self, *args, **kwargs):
        if self.pk is None:
           self.slug = slugify(self.name)
           return super(Category, self).save(*args, **kwargs)
        original = Category.objects.get(id=self.id)
        self.slug = slugify(self.name)
        if original.parent_id != self.parent_id:
           self.available = False
           super(Category, self).save(*args, **kwargs)
        if original.available != self.available:
            if self.available:
               for category in self.get_ancestors(include_self=False):
                   if category.available is False:
                      self.available = False
                      return
               return super(Category, self).save(*args, **kwargs)
            else:
                for category in self.get_descendants(include_self=True):   # Получаем потомков категории
                    category.available = False
                    super(Category, category).save(*args, **kwargs)
                return
        if original.slug != self.slug:
            super(Category, self).save(*args, **kwargs)
            for category in self.get_descendants(include_self=True):
                products = Product.objects.filter(category_id=category.id)
                for product in products:
                    product.save()
            return

        super(Category, self).save(*args, **kwargs)



class Attributes(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name = 'Главная категория',)
    name = models.CharField(max_length=200, db_index=True, verbose_name="Название")
    description = models.CharField(max_length=200, blank=True, verbose_name="Описание")
    available = models.BooleanField(default=True, verbose_name="Включить")

    class Meta:
        verbose_name = 'Атрибут категории'
        verbose_name_plural = 'Атрибуты категорий'
        ordering = ['name']

    def __str__(self):
        return self.name





# Модель продукта
class Product(models.Model):
    Type_Product = (
        ('P', 'Физический продукт'),
        ('S', 'Программный продукт'),
    )
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name = 'Главная категория',)
    type_product = models.CharField(default='P', max_length=200, choices=Type_Product, verbose_name="Тип продукта", help_text='Выберете тип объекта')
    name = models.CharField(max_length=200, unique = True, db_index=True, verbose_name="Название")
    slug_home = models.SlugField(default= 'Null', max_length=200, db_index=True)
    slug = models.SlugField( max_length=200, unique = True, default="")
    #image = models.ImageField(upload_to='product', blank=True, verbose_name="Изображение товара")
    description = models.TextField(blank=True, verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    stock = models.PositiveIntegerField(verbose_name="На складе")
    available = models.BooleanField(default=True, verbose_name="Доступен")
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    objects = models.Manager() # менеджер по умолчанию
    published = StatusManager() # переопределение менеджера модели


    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['name']


    def __str__(self):
        return self.name


    def get_absolute_url(self):
        return reverse('category:product_list', args=[self.slug_home + self.slug])

    def save(self, *args, **kwargs):
        if self.category_id:
           self.slug_home = self.category.get_path()
           self.slug = slugify(self.name)
           super(Product, self).save(*args, **kwargs)#def save(self, *args, **kwargs):




def upload_location_productimage(instance, filename):
    filebase, extension = filename.split('.')
    return 'product_img/%s/%s_%s.%s' % (instance.product_image.slug,instance.product_image.slug,slugify(instance.title_image), extension)

class ProductImage(models.Model):
    image = models.ImageField(upload_to=upload_location_productimage, blank=True, null=True, verbose_name='Изображение товара')
    product_image = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name = 'Продукт')
    title_image = models.CharField(max_length=200, db_index=True, verbose_name="Описание изображения", null=True, blank=False)

    class Meta:
        verbose_name = 'Изображение товара'
        verbose_name_plural = 'Изображения товаров'

    def __str__(self):
        return self.title_image

