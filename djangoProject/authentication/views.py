from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from .models import Profile

from .forms import CustomUserCreationForm


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Перенаправление на главную страницу или другую страницу
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password")
            return redirect(
                "login"
            )  # Перенаправляем обратно на страницу входа с сообщением об ошибке
    return render(request, "registration/login.html")


def logout_view(request):
    logout(request)
    # Перенаправление на страницу после выхода из системы
    return redirect("login")


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Создаем профиль пользователя
            Profile.objects.create(user=user)
            return redirect('login')  
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
