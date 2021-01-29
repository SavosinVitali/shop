from django.db.models.signals import post_delete, pre_save, post_save
from django.dispatch.dispatcher import receiver
from category.models import Brand, Product


@receiver(post_save, sender=Product)
def file_storage_resave_image(sender, instance, **kwargs):
    if instance.pk is not None and instance.name != instance._old_name:
        for name in instance.image.all():
            name.save(update_fields=['image', 'alt_image', 'title_image'])
        for name in instance.files.all():
            name.save(update_fields=['files'])

@receiver(post_save, sender=Brand)
def file_storage_resave_image2(sender, instance, **kwargs):
    if instance.pk is not None:
        if instance.name != instance._old_name or instance._old_country != instance.country:
            for product in Product.objects.filter(brand_id=instance.pk):
                for image in product.image.all():
                    image.save(update_fields=['image', 'alt_image', 'title_image'])
                for file in product.files.all():
                    file.save(update_fields=['files', 'title_files'])
