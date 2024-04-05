from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse

from .models import Profile
from .forms import ProfileForm, UserForm


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
    if request.method == "POST":
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile_exists = Profile.objects.filter(user=user).exists()
            if not profile_exists:
                profile = profile_form.save(commit=False)
                profile.user = user
                profile.save()
            login(request, user)
            return redirect(reverse("home"))
    else:
        user_form = UserForm()
        profile_form = ProfileForm()
    return render(
        request,
        "registration/register.html",
        {"user_form": user_form, "profile_form": profile_form},
    )
