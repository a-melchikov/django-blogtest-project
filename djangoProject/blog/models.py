from django.conf import settings
from django.db import models


# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=450)  # заголовок поста
    author = models.ForeignKey(  # Автор поста
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,  # Удаление поста
    )
    body = models.TextField()  # Поле нашего класса

    def __str__(self):
        return self.title
