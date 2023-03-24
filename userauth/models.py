from django.db import models
from django.contrib.auth.models import User
from post.models import Post
import PIL
from PIL import Image


def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    image = models.ImageField(upload_to=user_directory_path, default="default-user.png", null=True, blank=True,
                              verbose_name="image")
    favourite = models.ManyToManyField(Post, blank=True)
    bio = models.TextField(max_length=400, null=True, blank=True)
    url = models.URLField(max_length=1000, null=True, blank=True)
    location = models.CharField(max_length=50, null=True, blank=True)
    created = models.DateField(auto_now_add=True, null=True, blank=True)

    # def __str__(self):
    #     return self.first_name

    def __str__(self):
        return f'{self.user.username} - Profile'

    # reducing image size and quality

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #
    #     img = Image.open(self.image.path)
    #     if img.height > 300 or img.width > 300:
    #         output_size = (300, 300)
    #         img.thumbnail(output_size)
    #         img.save(self.image.path)
    #
    #
