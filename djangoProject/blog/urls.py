from django.urls import path
from .views import AboutPageView, BlogDetailView, BlogList, create_post

urlpatterns = [
    path("post/<int:pk>/", BlogDetailView.as_view(), name="post_detail"),
    path("about/", AboutPageView.as_view(), name="about"),
    path('create_post/', create_post, name='create_post'),
    path("", BlogList.as_view(), name="home"),
]
