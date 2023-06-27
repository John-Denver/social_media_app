from django.db import models
from django.contrib.auth.models import User
from django.db.models import Max


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="from_user")
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="to_user")
    body = models.TextField(default="")
    date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    @staticmethod
    def send_message(from_user, to_user, body):
        #         Sender message function
        sender_message = Message(
            user=from_user,
            sender=from_user,
            recipient=to_user,
            body=body,
            is_read=True
        )
        sender_message.save()
        #         Sender message function
        recipient_message = Message(
            user=to_user,
            sender=from_user,
            recipient=from_user,
            body=body,
            is_read=True
        )
        recipient_message.save()

        return sender_message

    @staticmethod
    def get_message(user):
        users = []
        messages = Message.objects.filter(user=user).values("recipient").annotate(last=Max('body')).order_by('-last')
        for message in messages:
            users.append({
                'user': User.objects.get(pk=message['recipient']),
                'last': message['last'],
                'unread': Message.objects.filter(user=user, recipient__pk=message['recipient'], is_read=False).count()
            })
        return users
