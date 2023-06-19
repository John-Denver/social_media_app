from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from notifications.models import Notification
from post.models import Post
import uuid


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)


def create_comment_notification(sender, instance, created, **kwargs):
    if created:
        comment = instance
        post = comment.post
        sender = comment.user
        recipient = post.user
        message = f"{sender.username} commented on your post: {comment.body}"
        Notification.objects.create(
            message=message,
            recipient=recipient,
            sender=sender,
            comment_body=comment.body,  # Set the comment body in the notification
            notification_type=2  # 2 represents a comment notification
        )


post_save.connect(create_comment_notification, sender=Comment)
