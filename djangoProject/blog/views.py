from django.contrib import messages
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
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
    return render(request, 'my_posts.html', {'user_posts': user_posts})


def edit_profile(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, "edit_profile.html", {"form": form})
