# Generated by Django 4.1.7 on 2023-06-21 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0006_alter_notification_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='timestamp',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]