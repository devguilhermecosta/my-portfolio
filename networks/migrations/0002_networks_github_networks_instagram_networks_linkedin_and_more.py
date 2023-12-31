# Generated by Django 4.2.7 on 2023-11-12 02:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('networks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='networks',
            name='github',
            field=models.CharField(default='', error_messages={'required': 'este campo é obrigatório'}, max_length=255),
        ),
        migrations.AddField(
            model_name='networks',
            name='instagram',
            field=models.CharField(default='', error_messages={'required': 'este campo é obrigatório'}, max_length=255),
        ),
        migrations.AddField(
            model_name='networks',
            name='linkedin',
            field=models.CharField(default='', error_messages={'required': 'este campo é obrigatório'}, max_length=255),
        ),
        migrations.AddField(
            model_name='networks',
            name='phone',
            field=models.CharField(default='', error_messages={'required': 'este campo é obrigatório'}, max_length=255),
        ),
        migrations.AddField(
            model_name='networks',
            name='whatsapp',
            field=models.CharField(default='', error_messages={'required': 'este campo é obrigatório'}, max_length=255),
        ),
        migrations.AlterField(
            model_name='networks',
            name='email',
            field=models.EmailField(default='', error_messages={'required': 'este campo é obrigatório'}, max_length=255),
        ),
    ]
