from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    date_of_birth = models.DateField(null=True, blank=True, verbose_name="Дата рождения")
    country = models.CharField(max_length=50, blank=True, verbose_name="Страна")
    city = models.CharField(max_length=50, blank=True, verbose_name="Город")
    registration_date = models.DateField(auto_now_add=True, verbose_name="Дата регистрации")
    bio = models.TextField(max_length=500, blank=True, verbose_name="О себе")
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True, verbose_name="Аватар")

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    def __str__(self):
        return self.user.username
