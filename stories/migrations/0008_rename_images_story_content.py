# Generated by Django 4.1.7 on 2023-05-22 16:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0007_rename_content_story_images'),
    ]

    operations = [
        migrations.RenameField(
            model_name='story',
            old_name='images',
            new_name='content',
        ),
    ]
