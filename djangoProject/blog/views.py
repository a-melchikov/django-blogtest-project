from django.views.generic import ListView, DetailView, TemplateView
from .models import Post


class BlogList(ListView):
    model = Post
    template = "home.html"


class BlogDetailView(DetailView):
    model = Post
    template = "post_detail.html"


class AboutPageView(TemplateView):
    template = "post_detail.html"
