# Generated by Django 4.1.7 on 2023-05-30 19:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0021_alter_media_object_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='media',
            name='media_type',
        ),
    ]