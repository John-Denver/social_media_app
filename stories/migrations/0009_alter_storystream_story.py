# Generated by Django 4.1.7 on 2023-05-25 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0008_rename_images_story_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storystream',
            name='story',
            field=models.ManyToManyField(related_name='stories', to='stories.story'),
        ),
    ]