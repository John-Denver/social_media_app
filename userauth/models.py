from django.db import models
from django.contrib.auth.models import User
from post.models import Post


def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    image = models.ImageField(upload_to=user_directory_path, null=True, blank=True, verbose_name="image")
    favourite = models.ManyToManyField(Post, blank=True, null=True)
    bio = models.TextField(max_length=400, null=True, blank=True)
    url = models.URLField(max_length=1000, null=True, blank=True)
    location = models.CharField(max_length=50, null=True, blank=True)
    created = models.DateField(auto_now_add=True)

    # def __str__(self):
    #     return self.first_name
