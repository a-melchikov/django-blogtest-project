from django.urls import path
from django.views.generic.base import RedirectView
from .views import (
    AboutPageView,
    AllProfilesView,
    BlogDetailView,
    BlogList,
    PostDeleteView,
    category_posts,
    create_post,
    delete_all_notifications,
    delete_notification,
    edit_post,
    edit_profile,
    like_post,
    mark_all_as_viewed,
    mark_as_viewed,
    my_posts,
    search_posts,
    send_message,
    inbox,
    subscribe,
    subscribed_posts,
    subscriber_list,
    unsubscribe,
    user_profile_view,
    notifications,
)

urlpatterns = [
    path("post/<int:pk>/", BlogDetailView.as_view(), name="post_detail"),
    path("post/<int:pk>/like/", like_post, name="like_post"),
    path("post/delete/<int:pk>/", PostDeleteView.as_view(), name="delete_post"),
    path("post/edit/<int:pk>/", edit_post, name="edit_post"),
    path("about/", AboutPageView.as_view(), name="about"),
    path("create_post/", create_post, name="create_post"),
    path("profiles/", AllProfilesView.as_view(), name="all_profiles"),
    path("profile/<str:user_name>/", user_profile_view, name="user_profile"),
    path("profile/<str:user_name>/edit/", edit_profile, name="edit_profile"),
    path("my_posts/", my_posts, name="my_posts"),
    path("catalog/", BlogList.as_view(), name="home"),
    path(
        "", RedirectView.as_view(pattern_name="home", permanent=False), name="blog_list"
    ),
    path("send_message/", send_message, name="send_message"),
    path("inbox/", inbox, name="inbox"),
    path("notifications/", notifications, name="notifications"),
    path("catalog/<slug:category_slug>/", category_posts, name="category_posts"),
    path("search/", search_posts, name="search_posts"),
    path(
        "delete_notification/<int:notification_id>/",
        delete_notification,
        name="delete_notification",
    ),
    path("subscribe/<int:author_id>/", subscribe, name="subscribe"),
    path("unsubscribe/<int:author_id>/", unsubscribe, name="unsubscribe"),
    path(
        "delete_all_notifications/",
        delete_all_notifications,
        name="delete_all_notifications",
    ),
    path(
        "mark_as_viewed/<int:notification_id>/", mark_as_viewed, name="mark_as_viewed"
    ),
    path("mark_all_as_viewed/", mark_all_as_viewed, name="mark_all_as_viewed"),
    path("subscribed_posts/", subscribed_posts, name="subscribed_posts"),
    path('subscribers/<str:username>/', subscriber_list, name='subscriber_list'),
]
