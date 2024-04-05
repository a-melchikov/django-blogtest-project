from django.shortcuts import redirect
from django.urls import reverse


class RedirectIfLoggedInMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Проверяем, авторизован ли пользователь
        if request.user.is_authenticated and request.path == reverse("login"):
            # Если пользователь уже авторизован и пытается зайти на страницу логина,
            # перенаправляем его на другую страницу, например, на домашнюю страницу
            return redirect("home")

        return response
