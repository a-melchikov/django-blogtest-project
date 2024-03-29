from django.urls import path
from .views import AboutPageView, BlogDetailView, BlogList, ProfilePageView, create_post

urlpatterns = [
    path("post/<int:pk>/", BlogDetailView.as_view(), name="post_detail"),
    path("about/", AboutPageView.as_view(), name="about"),
    path('create_post/', create_post, name='create_post'),
    path("profile/", ProfilePageView.as_view(), name="profile"),
    path("", BlogList.as_view(), name="home"),
]
