from django.db.models.signals import post_delete, pre_save, post_save, pre_delete
from django.dispatch.dispatcher import receiver
from file_storage.models import  Image_Storage, File_Storage



@receiver(pre_save, sender=File_Storage)
def file_rename(sender, instance, **kwargs):
    if instance.pk is not None:
        obj = sender.objects.get(pk=instance.pk)
        instance._old_files= obj.files
        instance._old_title_files = obj.title_files
        # names = upload_location_file(instance, old_self.files.url)
        if instance.pk is not None and instance.title_files != instance._old_title_files and instance.files.closed \
                or kwargs['update_fields'] == frozenset({'files'}):
            instance.files_renames()
            instance.files_renames_os()

        if instance.files and instance._old_files != instance.files:
            instance._old_files.close()
            instance._old_files.delete(False)


@receiver(pre_delete, sender=File_Storage)
def image_delete3(sender, instance, **kwargs):
    if instance.files:
        obj = sender.objects.get(pk=instance.pk)
        instance._old_files = obj.files
        instance._old_title_files = obj.title_files


@receiver(post_delete, sender=File_Storage)
def file_delete4(sender, instance, **kwargs):
    if instance.files:
       instance.delete_files()
       instance.folder_del()

@receiver(pre_save, sender=Image_Storage)
def image_rename(sender, instance, **kwargs):
    if instance.pk is not None:
        obj = sender.objects.get(pk=instance.pk)
        instance._old_image = obj.image
        instance._old_resize = obj.resize
        instance._old_title_image = obj.title_image
    if instance.image.closed is False:
        instance.image_convert_jpeg()
    if instance.pk is not None and instance.title_image != instance._old_title_image and instance.image.closed\
        or kwargs['update_fields'] == frozenset({'image'}):
        instance.image_renames()
        instance.image_renames_os()
    if instance._old_resize != instance.resize and not instance.resize:
        instance.delete_resize_image()
    if instance.image.closed is False and instance._old_image:
        instance.delete_image()

"""Функция  делает миниатюры согласно SIZES_IMAGE в Settings """
@receiver(post_save, sender=Image_Storage)
def resize_image(sender, instance, **kwargs):
    if instance.pk is not None and instance.image and instance.resize:
        instance.create_resize_image()


@receiver(pre_delete, sender=Image_Storage)
def image_delete1(sender, instance, **kwargs):
    if instance.image:
        obj = sender.objects.get(pk=instance.pk)
        instance._old_image = obj.image
        instance._old_resize = obj.resize
        instance._old_title_image = obj.title_image

@receiver(post_delete, sender=Image_Storage)
def image_delete2(sender, instance, **kwargs):
    instance.delete_image()
    instance.folder_del()


