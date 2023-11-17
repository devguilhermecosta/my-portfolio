from django.db import models
from django.db.models import Field
from django.utils.text import slugify


class Work(models.Model):
    title: Field = models.CharField(max_length=255)
    slug: models.Field = models.SlugField(unique=True)
    description: Field = models.TextField(max_length=1250)
    link: Field = models.URLField(max_length=255)
    cover: Field = models.ImageField(upload_to='works/covers/')
    created_at: models.Field = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class WorkImage(models.Model):
    work: models.Field = models.ForeignKey(Work,
                                           on_delete=models.CASCADE,
                                           blank=True,
                                           null=True,
                                           related_name='workimages',
                                           )
    image: models.Field = models.ImageField(
        upload_to='works/images/',  # type: ignore
        blank=True,
        null=True,
        )

    def __str__(self) -> str:
        return f'image_id {self.pk}'


# criar função para redimensionar as imagens
