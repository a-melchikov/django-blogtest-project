from django.contrib import messages
from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.generic import ListView

from authentication.models import Profile
from services.authentication_services import (
    authenticate_user,
    filter_user_posts,
    login_user,
    logout_user,
    create_user,
    get_user_by_username,
    get_user_posts,
    get_user_subscriptions,
    check_user_subscription,
    get_profile_form,
)
from .forms import ProfileForm, UserForm


def login_view(request):
    if request.method == "POST":
        username_or_email = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate_user(request, username_or_email, password)
        if user is not None:
            login_user(request, user)
            next_url = request.GET.get("next")
            if next_url:
                return redirect(next_url)
            else:
                return redirect("home")
        else:
            messages.error(
                request,
                "Неправильное имя пользователя или пароль. Пожалуйста, попробуйте снова.",
            )
            return redirect("login")
    next_url = request.GET.get("next")
    if next_url:
        messages.info(
            request,
            "Пожалуйста, войдите или зарегистрируйтесь, чтобы просмотреть профиль.",
        )
    return render(request, "registration/login.html")


def logout_view(request):
    if request.user.is_authenticated:
        logout_user(request)
        messages.error(request, "Вы успешно вышли из аккаунта")
    return redirect("login")


def register(request):
    if request.method == "POST":
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = create_user(user_form, profile_form)
            login_user(request, user)
            return redirect(reverse("home"))
    else:
        user_form = UserForm()
        profile_form = ProfileForm()
    return render(
        request,
        "registration/register.html",
        {"user_form": user_form, "profile_form": profile_form},
    )


@login_required
def edit_profile(request, user_name):
    user = get_user_by_username(user_name)

    if request.user != user:
        raise Http404("Вы не имеете прав на редактирование данного профиля")

    if request.method == "POST":
        form = get_profile_form(
            data=request.POST, files=request.FILES, instance=request.user.profile
        )
        if form.is_valid():
            form.save()
            return redirect("user_profile", user_name=request.user.username)
    else:
        form = get_profile_form(instance=request.user.profile)
    return render(request, "profile/edit_profile.html", {"form": form})


@login_required
def user_profile_view(request, user_name):
    user = get_user_by_username(user_name)
    user_posts = get_user_posts(user)
    is_subscribed = False
    subscriber_count = user.subscribers.count()

    if request.user.is_authenticated:
        subscribed_authors = get_user_subscriptions(request.user)
        user_posts = filter_user_posts(user_posts, request.user, subscribed_authors)
        is_subscribed = check_user_subscription(request.user, user)

    return render(
        request,
        "profile/profile.html",
        {
            "user": user,
            "user_posts": user_posts,
            "is_subscribed": is_subscribed,
            "subscriber_count": subscriber_count,
        },
    )


class AllProfilesView(ListView):
    model = Profile
    template_name = "profile/all_profiles.html"
    context_object_name = "profile_list"

    def get_queryset(self):
        return Profile.objects.all()
