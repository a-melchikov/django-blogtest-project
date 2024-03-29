from django.urls import path
from .views import AboutPageView, BlogDetailView, BlogList, ProfilePageView, create_post, edit_profile

urlpatterns = [
    path("post/<int:pk>/", BlogDetailView.as_view(), name="post_detail"),
    path("about/", AboutPageView.as_view(), name="about"),
    path('create_post/', create_post, name='create_post'),
    path("profile/", ProfilePageView.as_view(), name="profile"),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path("", BlogList.as_view(), name="home"),
]
