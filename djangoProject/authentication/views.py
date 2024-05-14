from django.contrib import messages
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse
from django.views.generic import ListView

from blog.models import Post

from .models import Profile
from .forms import ProfileForm, UserForm


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
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


@login_required
def edit_profile(request, user_name):
    user = get_object_or_404(User, username=user_name)

    if request.user != user:
        raise Http404("Вы не имеете прав на редактирование данного профиля")

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect("user_profile", user_name=request.user.username)
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, "profile/edit_profile.html", {"form": form})


@login_required
def user_profile_view(request, user_name):
    user = get_object_or_404(User, username=user_name)
    user_posts = Post.objects.filter(author=user).order_by("-publish_date")

    subscribed_authors = request.user.subscriptions.values_list("author__id", flat=True)
    user_posts = user_posts.filter(
        Q(for_subscribers=False)
        | Q(author__id__in=subscribed_authors)
        | Q(author=request.user)
    )

    is_subscribed = False
    if request.user.is_authenticated:
        is_subscribed = request.user.subscriptions.filter(author=user).exists()
    subscriber_count = user.subscribers.count()
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
