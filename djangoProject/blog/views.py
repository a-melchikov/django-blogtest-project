from django.views.generic import ListView, DetailView, TemplateView
from .models import Post


class BlogList(ListView):
    model = Post
    template_name = "home.html"


class BlogDetailView(DetailView):
    model = Post
    template_name = "post_detail.html"


class AboutPageView(TemplateView):
    template_name = "about.html"
