from django.urls import path
from django.views.generic.base import RedirectView
from .views import (
    AboutPageView,
    BlogDetailView,
    BlogList,
    PostDeleteView,
    category_posts,
    create_post,
    edit_post,
    favorite_posts,
    like_post,
    my_posts,
    search_posts,
    subscribed_posts,
    toggle_favorite,
)

urlpatterns = [
    path("post/<int:pk>/", BlogDetailView.as_view(), name="post_detail"),
    path("post/<int:pk>/like/", like_post, name="like_post"),
    path("post/delete/<int:pk>/", PostDeleteView.as_view(), name="delete_post"),
    path("post/edit/<int:pk>/", edit_post, name="edit_post"),
    path("about/", AboutPageView.as_view(), name="about"),
    path("create_post/", create_post, name="create_post"),
    path("my_posts/", my_posts, name="my_posts"),
    path("catalog/", BlogList.as_view(), name="home"),
    path(
        "", RedirectView.as_view(pattern_name="home", permanent=False), name="blog_list"
    ),
    path("catalog/<slug:category_slug>/", category_posts, name="category_posts"),
    path("search/", search_posts, name="search_posts"),
    path("subscribed_posts/", subscribed_posts, name="subscribed_posts"),
    path("toggle_favorite/<int:post_id>/", toggle_favorite, name="toggle_favorite"),
    path("favorite-posts/", favorite_posts, name="favorite_posts"),
]
