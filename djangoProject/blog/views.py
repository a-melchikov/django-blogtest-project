from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from .models import Post
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


class ProfilePageView(TemplateView):
    template_name = "profile.html"


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


def my_posts(request):
    # Получаем все посты текущего пользователя
    user = request.user
    user_posts = Post.objects.filter(author=user)
    return render(request, "my_posts.html", {"user_posts": user_posts})


def edit_profile(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = ProfileForm(instance=request.user.profile)
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
