from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    age = models.IntegerField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True)
    country = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=50, blank=True)
    registration_date = models.DateField(auto_now_add=True)
    bio = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.user.username


# Указываем явные имена обратных доступов для groups и user_permissions
CustomUser.groups.field.remote_field.related_name = "custom_user_set"
CustomUser.user_permissions.field.remote_field.related_name = "custom_user_set"
