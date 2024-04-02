from django.urls import path
from django.views.generic.base import RedirectView
from .views import (
    AboutPageView,
    BlogDetailView,
    BlogList,
    PostDeleteView,
    ProfilePageView,
    create_post,
    edit_post,
    edit_profile,
    my_posts,
    send_message,
    inbox,
)

urlpatterns = [
    path("post/<int:pk>/", BlogDetailView.as_view(), name="post_detail"),
    path("post/delete/<int:pk>/", PostDeleteView.as_view(), name="delete_post"),
    path("post/edit/<int:pk>/", edit_post, name="edit_post"),
    path("about/", AboutPageView.as_view(), name="about"),
    path("create_post/", create_post, name="create_post"),
    path("profile/", ProfilePageView.as_view(), name="profile"),
    path("profile/edit/", edit_profile, name="edit_profile"),
    path("my_posts/", my_posts, name="my_posts"),
    path("catalog/", BlogList.as_view(), name="home"),
    path("", RedirectView.as_view(pattern_name='home', permanent=False)),
    path("send_message/", send_message, name="send_message"),
    path("inbox/", inbox, name="inbox"),
]
