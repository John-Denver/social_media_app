# Generated by Django 4.1.7 on 2023-05-17 19:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0016_alter_story_id'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Story',
        ),
    ]