# Generated by Django 3.1.7 on 2021-11-19 00:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0002_auto_20211119_0949'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='community',
            new_name='review',
        ),
    ]