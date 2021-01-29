from django.db.models.signals import post_delete, pre_save, post_save, pre_delete
from django.dispatch.dispatcher import receiver
from file_storage.models import  Image_Storage, File_Storage



@receiver(pre_save, sender=File_Storage)
def file_rename(sender, instance, **kwargs):
    instance.title_files_generator()
    if instance.pk is not None:
        obj = sender.objects.get(pk=instance.pk)
        instance._old_files = obj.files
        instance._old_title_files = obj.title_files
        # names = upload_location_file(instance, old_self.files.url)
        if instance.pk is not None and instance._old_file_type != instance.file_type and instance.files.closed \
                or kwargs['update_fields'] == frozenset({'files'}):
            instance.files_renames()
            instance.files_renames_os()

        if instance.files and instance._old_files != instance.files:
            instance._old_files.close()
            instance.delete_files()




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
    instance.alt_image_generator()
    instance.title_image_generator()
    instance.my_flag = False
    """Если создали файл"""
    if instance.image.closed is False:
        instance.image_convert_jpeg()
        if instance._old_image:
            obj = sender.objects.get(pk=instance.pk)
            instance._old_image=obj._old_image
            instance.delete_image()
            if instance.resize and obj._old_resize:
                instance.my_flag = True
        return
    """Если произошло изменение названия продукта или брэнда"""
    if instance.pk is not None and instance.image.closed or kwargs['update_fields']:
        instance.image_renames()
        instance.image_renames_os()
    """Если произошло изменение делать миниатюры, удаляет файлы миниатюр"""
    if instance._old_image and instance._old_resize != instance.resize and not instance.resize:
        instance.image_renames()
        instance.delete_resize_image()
    """Если произошло изменение делать миниатюры, создает файлы миниатюр"""
    if instance._old_resize != instance.resize and instance.resize:
        instance.image_renames()
    """Удаляет старые файлы если вабрано новое изображение"""
    if instance.image.closed is False and instance._old_image:
        instance.delete_image()


"""Функция  делает миниатюры согласно SIZES_IMAGE в Settings """
@receiver(post_save, sender=Image_Storage)
def resize_image(sender, instance, **kwargs):
    if instance.pk is not None and instance.image and instance._old_resize != instance.resize and instance.resize \
            and not kwargs['update_fields'] or kwargs['created'] and instance.resize or instance.my_flag:
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


