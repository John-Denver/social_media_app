# Generated by Django 4.1.7 on 2023-05-10 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0012_alter_tag_options_remove_post_tag_remove_tag_title_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='posted',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
