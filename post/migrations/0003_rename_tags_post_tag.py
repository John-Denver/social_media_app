# Generated by Django 4.1.7 on 2023-03-06 19:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0002_stream_post'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='tags',
            new_name='tag',
        ),
    ]
