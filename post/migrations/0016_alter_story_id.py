# Generated by Django 4.1.7 on 2023-05-12 12:15

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0015_alter_story_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='story',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
