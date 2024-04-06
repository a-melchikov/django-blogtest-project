from django.urls import path
from django.views.generic.base import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    AboutPageView,
    AllProfilesView,
    BlogDetailView,
    BlogList,
    PostDeleteView,
    create_post,
    edit_post,
    edit_profile,
    my_posts,
    send_message,
    inbox,
    user_profile_view,
)

urlpatterns = [
    path("post/<int:pk>/", BlogDetailView.as_view(), name="post_detail"),
    path("post/delete/<int:pk>/", PostDeleteView.as_view(), name="delete_post"),
    path("post/edit/<int:pk>/", edit_post, name="edit_post"),
    path("about/", AboutPageView.as_view(), name="about"),
    path("create_post/", create_post, name="create_post"),
    path("profiles/", AllProfilesView.as_view(), name="all_profiles"),
    path("profile/<str:user_name>/", user_profile_view, name="user_profile"),
    path("profile/edit/", edit_profile, name="edit_profile"),
    path("my_posts/", my_posts, name="my_posts"),
    path("catalog/", BlogList.as_view(), name="home"),
    path("", RedirectView.as_view(pattern_name="home", permanent=False)),
    path("send_message/", send_message, name="send_message"),
    path("inbox/", inbox, name="inbox"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
