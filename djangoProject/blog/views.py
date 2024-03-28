from django.views.generic import ListView, DetailView, TemplateView
from .models import Post
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from blog.forms import PostForm


class BlogList(ListView):
    model = Post
    template_name = "home.html"


class BlogDetailView(DetailView):
    model = Post
    template_name = "post_detail.html"


class AboutPageView(TemplateView):
    template_name = "about.html"

@login_required  # Декоратор, чтобы требовать аутентификацию пользователя
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')  # Перенаправляем пользователя на главную страницу после создания поста
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})
