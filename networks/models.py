from django.db import models
from django.db.models import Field


class Networks(models.Model):
    instagram: Field = models.CharField(max_length=255, blank=True)
    linkedin: Field = models.CharField(max_length=255, blank=True)
    github: Field = models.CharField(max_length=255, blank=True)
    whatsapp: Field = models.CharField(max_length=255, blank=True)
    phone: Field = models.CharField(max_length=255, blank=True)
    email: Field = models.EmailField(max_length=255, blank=True)
