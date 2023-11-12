from django.db import models
from django.db.models import Field


error_messages = {
    'required': 'este campo é obrigatório',
}


class Networks(models.Model):
    instagram: Field = models.CharField(max_length=255,
                                        blank=False,
                                        null=False,
                                        default='',
                                        error_messages=error_messages,
                                        )
    linkedin: Field = models.CharField(max_length=255,
                                       blank=False,
                                       null=False,
                                       default='',
                                       error_messages=error_messages,
                                       )
    github: Field = models.CharField(max_length=255,
                                     blank=False,
                                     null=False,
                                     default='',
                                     error_messages=error_messages,
                                     )
    whatsapp: Field = models.CharField(max_length=255,
                                       blank=False,
                                       null=False,
                                       default='',
                                       error_messages=error_messages,
                                       )
    phone: Field = models.CharField(max_length=255,
                                    blank=False,
                                    null=False,
                                    default='',
                                    error_messages=error_messages,
                                    )
    email: Field = models.EmailField(max_length=255,
                                     blank=False,
                                     null=False,
                                     default='',
                                     error_messages=error_messages,
                                     )
