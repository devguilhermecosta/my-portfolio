# Generated by Django 4.2.7 on 2023-11-15 01:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('networks', '0005_alter_networks_email_alter_networks_github_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='networks',
            name='instagram',
            field=models.CharField(error_messages={'blank': 'bla bla bla'}, max_length=255),
        ),
    ]
