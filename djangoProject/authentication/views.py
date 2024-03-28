from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

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
    return render(request, "authentication/login.html")


def logout_view(request):
    logout(request)
    # Перенаправление на страницу после выхода из системы
    return redirect("login")


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(
                "login"
            )  # Перенаправление на страницу входа после успешной регистрации
    else:
        form = CustomUserCreationForm()
    return render(request, "registration/register.html", {"form": form})
