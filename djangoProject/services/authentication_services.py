from typing import List, Optional

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Q, QuerySet
from django.http import HttpRequest
from django.shortcuts import get_object_or_404

from blog.models import Post
from authentication.forms import ProfileForm, UserForm
from authentication.models import Profile


def authenticate_user(
    request: HttpRequest, username_or_email: str, password: str
) -> Optional[User]:
    """
    Аутентифицирует пользователя по имени пользователя или email и паролю.

    args:
        request (HttpRequest): Объект запроса.
        username_or_email (str): Имя пользователя или email.
        password (str): Пароль.

    return:
        Optional[User]: Аутентифицированный пользователь или None, если аутентификация не удалась.
    """
    try:
        user = User.objects.get(email=username_or_email)
        username = user.username
    except User.DoesNotExist:
        username = username_or_email

    return authenticate(request, username=username, password=password)


def login_user(request: HttpRequest, user: User) -> None:
    """
    Выполняет вход пользователя в систему.

    args:
        request (HttpRequest): Объект запроса.
        user (User): Пользователь, который будет залогинен.
    """
    login(request, user)


def logout_user(request: HttpRequest) -> None:
    """
    Выполняет выход пользователя из системы.

    args:
        request (HttpRequest): Объект запроса.
    """
    logout(request)


def create_user(user_form: UserForm, profile_form: ProfileForm) -> User:
    """
    Создает нового пользователя и профиль.

    args:
        user_form (UserForm): Форма создания пользователя.
        profile_form (ProfileForm): Форма создания профиля.

    return:
        User: Созданный пользователь.
    """
    user = user_form.save()
    profile_exists = Profile.objects.filter(user=user).exists()
    if not profile_exists:
        profile = profile_form.save(commit=False)
        profile.user = user
        profile.save()
    return user


def get_user_by_username(username: str) -> User:
    """
    Получает пользователя по имени пользователя.

    args:
        username (str): Имя пользователя.

    return:
        User: Найденный пользователь.
    """
    return get_object_or_404(User, username=username)


def get_user_posts(user: User) -> QuerySet[Post]:
    """
    Получает посты пользователя, отсортированные по дате публикации.

    args:
        user (User): Пользователь, чьи посты нужно получить.

    return:
        QuerySet[Post]: Запрос, содержащий посты пользователя.
    """
    return Post.objects.filter(author=user).order_by("-publish_date")


def get_user_subscriptions(user: User) -> QuerySet[int]:
    """
    Получает список ID авторов, на которых подписан пользователь.

    args:
        user (User): Пользователь, чьи подписки нужно получить.

    return:
        QuerySet[int]: Запрос, содержащий ID авторов.
    """
    return user.subscriptions.values_list("author__id", flat=True)


def check_user_subscription(request_user: User, target_user: User) -> bool:
    """
    Проверяет, подписан ли один пользователь на другого.

    args:
        request_user (User): Пользователь, для которого проверяется подписка.
        target_user (User): Пользователь, на которого проверяется подписка.

    return:
        bool: True, если request_user подписан на target_user, иначе False.
    """
    return request_user.subscriptions.filter(author=target_user).exists()


def get_profile_form(
    instance: Optional[Profile] = None,
    data: Optional[dict] = None,
    files: Optional[dict] = None,
) -> ProfileForm:
    """
    Создает и возвращает форму профиля.

    args:
        instance (Optional[Profile]): Экземпляр профиля (по умолчанию None).
        data (Optional[dict]): Данные для заполнения формы (по умолчанию None).
        files (Optional[dict]): Файлы для заполнения формы (по умолчанию None).

    return:
        ProfileForm: Экземпляр формы профиля.
    """
    return ProfileForm(instance=instance, data=data, files=files)


def get_user_profile(user_name: str) -> Profile:
    """
    Получает профиль пользователя по имени пользователя.

    args:
        user_name (str): Имя пользователя.

    return:
        Profile: Найденный профиль пользователя.
    """
    return get_object_or_404(User, username=user_name).profile


def filter_user_posts(
    user_posts: QuerySet[Post], user: User, subscribed_authors: List[int]
) -> QuerySet[Post]:
    """
    Фильтрует посты пользователя в зависимости от статуса подписки.

    args:
        user_posts (QuerySet[Post]): Набор постов пользователя для фильтрации.
        user (User): Пользователь, для которого выполняется фильтрация.
        subscribed_authors (List[int]): Список ID авторов, на которых подписан пользователь.

    return:
        QuerySet[Post]: Отфильтрованный набор постов.
    """
    return user_posts.filter(
        Q(for_subscribers=False) | Q(author__id__in=subscribed_authors) | Q(author=user)
    )
