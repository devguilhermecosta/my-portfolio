from django.db import models
from django.db.models import Field
from django.utils.text import slugify
from utils.images import resize_image
import contextlib


class Work(models.Model):
    title: Field = models.CharField(max_length=255, unique=True)
    slug: models.Field = models.SlugField(unique=True, blank=True, null=True)
    description: Field = models.TextField(max_length=1250)
    link: Field = models.URLField(max_length=255, blank=True, null=True)
    cover: Field = models.ImageField(upload_to='works/covers/')
    created_at: models.Field = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = slugify(self.title)

        if self.cover:
            with contextlib.suppress(FileNotFoundError):
                resize_image(self.cover)

        return super().save(*args, **kwargs)


class WorkImage(models.Model):
    work: models.Field = models.ForeignKey(Work,
                                           on_delete=models.CASCADE,
                                           related_name='workimages',
                                           )
    image: models.Field = models.ImageField(upload_to='works/images/')

    def __str__(self) -> str:
        return f'image_id {self.pk}'

    def save(self, *args, **kwargs) -> None:
        if self.image:
            with contextlib.suppress(FileNotFoundError):
                resize_image(self.image)

        return super().save(*args, **kwargs)
