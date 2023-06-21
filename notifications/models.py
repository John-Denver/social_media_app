from datetime import timezone

from django.db import models
from django.contrib.auth.models import User


class Notification(models.Model):
    NOTIFICATION_TYPES = ((1, 'Like'), (2, 'Comment'), (3, 'Follow'))
    post = models.ForeignKey('post.Post', on_delete=models.CASCADE, related_name="noti_post", blank=True, null=True)
    message = models.CharField(max_length=255)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="noti_to_user")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="noti_from_user")
    notification_type = models.IntegerField(choices=NOTIFICATION_TYPES)
    comment_body = models.CharField(max_length=50, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"From: {self.sender.username} | To: {self.recipient.username} | Message: {self.message}"


