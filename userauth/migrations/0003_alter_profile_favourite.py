# Generated by Django 4.1.7 on 2023-03-11 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0005_alter_post_id'),
        ('userauth', '0002_profile_bio_profile_created_profile_first_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='favourite',
            field=models.ManyToManyField(blank=True, null=True, to='post.post'),
        ),
    ]
