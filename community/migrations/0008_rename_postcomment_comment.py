# Generated by Django 3.2.9 on 2021-11-19 01:38

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('community', '0007_auto_20211119_1037'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PostComment',
            new_name='Comment',
        ),
    ]