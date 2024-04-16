from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from .views import login_view, logout_view, register

urlpatterns = [
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("register/", register, name="register"),
]
