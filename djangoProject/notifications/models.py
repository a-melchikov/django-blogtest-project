from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Notification(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="received_notifications",
    )
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Отправитель",
        related_name="sent_notifications",
        default=None,
    )
    sender_name = models.CharField(
        max_length=255, default="", verbose_name="Имя отправителя"
    )
    message = models.TextField(verbose_name="Сообщение")
    text = models.CharField(max_length=255, null=True)
    type = models.CharField(max_length=255, null=True)
    timestamp = models.DateTimeField(default=timezone.now, verbose_name="Дата и время")
    is_new = models.BooleanField(default=True, verbose_name="Новое уведомление")
    viewed = models.BooleanField(default=False, verbose_name="Просмотрено")

    class Meta:
        verbose_name = "Уведомление"
        verbose_name_plural = "Уведомления"

    def __str__(self):
        return self.message
