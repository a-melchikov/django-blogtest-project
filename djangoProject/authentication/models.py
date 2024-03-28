from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    age = models.IntegerField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)


# Указываем явные имена обратных доступов для groups и user_permissions
CustomUser.groups.field.remote_field.related_name = "custom_user_set"
CustomUser.user_permissions.field.remote_field.related_name = "custom_user_set"
