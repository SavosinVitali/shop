from django.db.models.signals import post_delete
from django.dispatch.dispatcher import receiver
from category.models import Brand

@receiver(post_delete, sender=Brand)
def logo_delete(sender, instance, **kwargs):
    if instance.logo.name:
       instance.logo.delete(False)