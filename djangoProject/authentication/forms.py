from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Profile


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ["username", "email", "age"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.save()
        profile = Profile.objects.create(user=user)  # Создание профиля
        return user