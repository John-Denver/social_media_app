# Generated by Django 4.1.7 on 2023-05-30 19:09

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0020_alter_media_object_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='media',
            name='object_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]
