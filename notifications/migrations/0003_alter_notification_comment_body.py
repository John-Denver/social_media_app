# Generated by Django 4.1.7 on 2023-06-19 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0002_notification_comment_body'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='comment_body',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]