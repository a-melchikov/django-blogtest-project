from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User

from authentication.models import Profile

from .models import Message, Post
from .forms import PostForm, ProfileForm


class BlogList(ListView):
    model = Post
    template_name = "home.html"

    def get_queryset(self):
        return Post.objects.all()


class BlogDetailView(DetailView):
    model = Post
    template_name = "post_detail.html"


class AboutPageView(TemplateView):
    template_name = "about.html"


@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("home")
    else:
        form = PostForm()
    return render(request, "create_post.html", {"form": form})


@login_required
def my_posts(request):
    # Получаем все посты текущего пользователя
    user = request.user
    user_posts = Post.objects.filter(author=user)
    return render(request, "my_posts.html", {"user_posts": user_posts})


@login_required
def edit_profile(request, user_name):
    user = get_object_or_404(User, username=user_name)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=user.profile)
        if form.is_valid():
            form.save()
            return redirect("user_profile", user_name=request.user.username)
    else:
        form = ProfileForm(instance=user.profile)
    return render(request, "edit_profile.html", {"form": form})


@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect("my_posts")
    else:
        form = PostForm(instance=post)
    return render(request, "edit_post.html", {"form": form})


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy(
        "my_posts"
    )  # После успешного удаления перенаправить на страницу с моими постами
    template_name = (
        "post_confirm_delete.html"  # Создайте шаблон подтверждения удаления поста
    )


@login_required
def inbox(request):
    messages = Message.objects.filter(recipient=request.user).order_by("-timestamp")
    return render(request, "inbox.html", {"messages": messages})


@login_required
def send_message(request):
    if request.method == "POST":
        recipient = request.POST["recipient"]
        subject = request.POST["subject"]
        body = request.POST["body"]
        message = Message(
            sender=request.user,
            recipient=Profile.objects.get(user__username=recipient).user,
            subject=subject,
            body=body,
        )
        message.save()
        return redirect("inbox")
    else:
        profiles = Profile.objects.all()
        return render(request, "send_message.html", {"profiles": profiles})


def user_profile_view(request, user_name):
    # Получаем пользователя по его имени или возвращаем 404 ошибку, если пользователь не найден
    user = get_object_or_404(User, username=user_name)
    # Здесь можно передать данные о пользователе в шаблон для отображения
    return render(request, "profile.html", {"user": user})


class AllProfilesView(ListView):
    model = Profile
    template_name = "all_profiles.html"
    context_object_name = "profile_list"

    def get_queryset(self):
        return Profile.objects.all()
