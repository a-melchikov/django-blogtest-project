from django.urls import path
from .views import AboutPageView, BlogDetailView, BlogList

urlpatterns = [
    path("post/<int:pk>/", BlogList.as_view(), name="post_detail"),
    path("about/", AboutPageView.as_view(), name="post_detail"),
    path("", BlogDetailView.as_view(), name="home"),
]
