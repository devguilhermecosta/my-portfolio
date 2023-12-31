# Generated by Django 4.2.7 on 2023-11-15 01:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('networks', '0003_alter_networks_email_alter_networks_github_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='networks',
            name='email',
            field=models.EmailField(error_messages={'blank': 'campo é obrigatório', 'required': 'campo é obrigatório'}, max_length=255),
        ),
        migrations.AlterField(
            model_name='networks',
            name='github',
            field=models.CharField(error_messages={'blank': 'campo é obrigatório', 'required': 'campo é obrigatório'}, max_length=255),
        ),
        migrations.AlterField(
            model_name='networks',
            name='instagram',
            field=models.CharField(error_messages={'blank': 'campo é obrigatório', 'required': 'campo é obrigatório'}, max_length=255),
        ),
        migrations.AlterField(
            model_name='networks',
            name='linkedin',
            field=models.CharField(error_messages={'blank': 'campo é obrigatório', 'required': 'campo é obrigatório'}, max_length=255),
        ),
        migrations.AlterField(
            model_name='networks',
            name='phone',
            field=models.CharField(error_messages={'blank': 'campo é obrigatório', 'required': 'campo é obrigatório'}, max_length=255),
        ),
        migrations.AlterField(
            model_name='networks',
            name='whatsapp',
            field=models.CharField(error_messages={'blank': 'campo é obrigatório', 'required': 'campo é obrigatório'}, max_length=255),
        ),
    ]
