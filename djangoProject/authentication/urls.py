from django.urls import path
from .views import (
    AllProfilesView,
    edit_profile,
    login_view,
    logout_view,
    register,
    user_profile_view,
)

urlpatterns = [
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("register/", register, name="register"),
    path("profiles/", AllProfilesView.as_view(), name="all_profiles"),
    path("profile/<str:user_name>/", user_profile_view, name="user_profile"),
    path("profile/<str:user_name>/edit/", edit_profile, name="edit_profile"),
]
