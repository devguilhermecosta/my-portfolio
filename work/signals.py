from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from .models import Work, WorkImage
import os
import contextlib


def delete_image(instance: Work | WorkImage | None) -> None:
    if instance is not None:
        with contextlib.suppress(ValueError, FileNotFoundError):
            if isinstance(instance, Work):
                os.remove(instance.cover.path)
            else:
                os.remove(instance.image.path)


@receiver(pre_delete, sender=Work)
def work_cover_delete(sender, instance, *args, **kwargs) -> None:
    old_instance = Work.objects.filter(pk=instance.pk).first()
    delete_image(old_instance)


@receiver(pre_save, sender=Work)
def work_cover_update(sender, instance: Work, *args, **kwargs) -> None:
    old_instance = Work.objects.filter(pk=instance.pk).first()

    if old_instance is not None:
        new_instance = old_instance.cover != instance.cover

        if new_instance:
            delete_image(old_instance)


@receiver(pre_delete, sender=WorkImage)
def workimage_image_delete(sender, instance, *args, **kwargs) -> None:
    old_instance = WorkImage.objects.filter(pk=instance.pk).first()
    delete_image(old_instance)
