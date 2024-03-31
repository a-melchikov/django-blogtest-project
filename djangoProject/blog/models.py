from django.conf import settings
from django.db import models
from django.utils import timezone
from authentication.models import CustomUser


class Post(models.Model):
    title = models.CharField(max_length=450)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    body = models.TextField()
    publish_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class Message(models.Model):
    sender = models.ForeignKey(
        CustomUser, related_name="sent_messages", on_delete=models.CASCADE
    )
    recipient = models.ForeignKey(
        CustomUser, related_name="received_messages", on_delete=models.CASCADE
    )
    subject = models.CharField(max_length=200)
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return self.subject
