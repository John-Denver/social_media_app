# Generated by Django 4.1.7 on 2023-05-17 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0004_alter_story_user_alter_storystream_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='story',
            name='caption',
            field=models.CharField(max_length=105),
        ),
    ]
