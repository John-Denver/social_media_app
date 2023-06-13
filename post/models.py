from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.utils.text import slugify
from django.urls import reverse
import uuid
import os
# from django.contrib.postgres.fields import ArrayField
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation


# uploads user files to a specific directory
def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)


def story_directory_path(instance, filename):
    return 'story_{0}/{1}'.format(instance.user.id, filename)


class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=100, unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Tag, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


# Get the files posted and check if they are images or videos

class Media(models.Model):
    MEDIA_TYPES = (
        ('image', 'Image'),
        ('video', 'Video'),
    )

    file = models.FileField(upload_to=user_directory_path)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='media')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField(default=uuid.uuid4, editable=False)
    content_object = GenericForeignKey('content_type', 'object_id')
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def save(self, *args, **kwargs):
        ext = os.path.splitext(self.file.name)[1].lower()

        if ext in ['.jpg', '.jpeg', '.png', '.gif']:
            self.media_type = 'image'
        elif ext in ['.mp4', '.mov', '.avi']:
            self.media_type = 'video'

        super().save(*args, **kwargs)


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    media = GenericRelation(Media, related_query_name='posts')
    caption = models.CharField(max_length=10000, verbose_name="caption")
    posted = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='likes', blank=True, default=None)
    like_count = models.BigIntegerField(default=0)

    # likes = models.IntegerField(default=0)

    # def get_absolute_url(self):
    #     return reverse("post_detail", args=[str(self.id)])

    def __str__(self):
        return str(self.caption)


class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')


# when you follow a user you get to stream/see what they have posted
# like on the main page and not on their page
# stream is the main page
class Stream(models.Model):
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stream_following')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="stream_user")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField()

    def add_post(sender, instance, *args, **kwargs):
        post = instance
        user = post.user
        followers = Follow.objects.all().filter(following=user)
        for follower in followers:
            stream = Stream(post=post, user=follower.follower, date=post.posted, following=user)
            stream.save()


# class Like(models.Model):
#     user = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)
#     post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)

# class Likes(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
#     post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")


post_save.connect(Stream.add_post, sender=Post)

#
# class Story(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="story")
#     title = models.CharField(max_length=255)
#     content = models.TextField(blank=True, null=True)
#     image = models.ImageField(upload_to=story_directory_path, null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return self.title
