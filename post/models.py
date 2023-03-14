from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.utils.text import slugify
from django.urls import reverse
import uuid


# uploads user files to a specific directory
def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)


# the way instagram has hashtags.....here is the code
class Tag(models.Model):
    title = models.CharField(max_length=100, verbose_name="Tag")
    slug = models.SlugField(null=False, unique=True, default=uuid.uuid1)

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    # when a user clicks on a Tag/hashtag it should take him to a page that has other posts with the same tag/hashtag
    # code for that below

    # def get_absolute_url(self):
    #     return reverse('tags', args=[self.slug])

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug - slugify(self.slug)
        return super().save(*args, **kwargs)


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    picture = models.ImageField(upload_to=user_directory_path, verbose_name="picture")
    caption = models.CharField(max_length=10000, verbose_name="caption")
    posted = models.DateField(auto_now_add=True)
    tag = models.ManyToManyField(Tag, related_name="tags", blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse("post_detail", args=[str(self.id)])

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


class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_likes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_likes")


post_save.connect(Stream.add_post, sender=Post)
