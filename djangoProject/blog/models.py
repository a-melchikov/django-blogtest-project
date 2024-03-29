from django.conf import settings
from django.db import models
from authentication.models import CustomUser


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True)
    country = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=50, blank=True)
    registration_date = models.DateField(auto_now_add=True)
    bio = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.user.username


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
