from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # Добавьте здесь дополнительные поля, если необходимо
    pass

# Указываем явные имена обратных доступов для groups и user_permissions
CustomUser.groups.field.remote_field.related_name = 'custom_user_set'
CustomUser.user_permissions.field.remote_field.related_name = 'custom_user_set'
