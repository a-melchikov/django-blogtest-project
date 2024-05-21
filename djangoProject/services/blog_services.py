from typing import Any, Dict
from django.db.models import QuerySet, Q
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import reverse, get_object_or_404

from blog.models import Post, Comment, Category, Favorite
from blog.forms import CommentForm, PostForm
from notifications.models import Notification
from subscriptions.models import Subscription
from services.paginators import GeneralPaginator


def get_blog_queryset(user: User, ordering: str) -> QuerySet[Post]:
    """
    Получает queryset постов в блоге для отображения.

    args:
            user (User): Текущий пользователь.
            ordering (str): Порядок сортировки.

    return:
            QuerySet[Post]: QuerySet постов.
    """
    queryset = Post.objects.all()
    if user.is_authenticated:
        subscribed_authors = user.subscriptions.values_list("author__id", flat=True)
        queryset = queryset.filter(
            Q(for_subscribers=False)
            | Q(author__id__in=subscribed_authors)
            | Q(author=user)
        ).order_by(ordering)
    else:
        queryset = queryset.filter(for_subscribers=False).order_by(ordering)
    return queryset


def get_blog_context(
    user: User, posts: QuerySet[Post], paginator, page_number: int
) -> Dict[str, Any]:
    """
    Формирует контекст данных для отображения постов в блоге.

    args:
            user (User): Текущий пользователь.
            posts (QuerySet[Post]): QuerySet постов.
            paginator: Объект пагинатора.
            page_number (int): Номер текущей страницы.

    return:
            Dict[str, Any]: Контекст данных.
    """
    page_obj = paginator.get_page(page_number)
    context = {"posts": page_obj}

    if user.is_authenticated:
        authors = {post.author_id: post.author for post in page_obj.object_list}
        author_subscribers = {
            author_id: list(
                User.objects.filter(subscriptions__subscriber=user, id=author_id)
            )
            for author_id in authors.keys()
        }
        context["author_subscribers"] = author_subscribers

    return context


def get_post_comments(post: Post) -> QuerySet[Comment]:
    """
    Получает утвержденные комментарии для поста.

    args:
            post (Post): Пост для которого получаем комментарии.

    return:
            QuerySet[Comment]: QuerySet комментариев.
    """
    return post.comments.filter(approved_comment=True).order_by("-created_date")


def handle_comment_form(request, post: Post) -> CommentForm:
    """
    Обрабатывает форму комментария и сохраняет комментарий и уведомления.

    args:
            request: HTTP запрос.
            post (Post): Пост для которого добавляется комментарий.

    return:
            CommentForm: Форма комментария.
    """
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()
        categories = request.POST.getlist("categories")
        if categories:
            post.categories.add(*categories)
        _create_notifications(post, request.user, comment.text)
    return form


def _create_notifications(post: Post, user: User, comment_text: str):
    """
    Создает уведомления для автора поста о новом комментарии.

    args:
            post (Post): Пост для которого добавлен комментарий.
            user (User): Пользователь, добавивший комментарий.
            comment_text (str): Текст комментария.
    """
    sender_name = user.username
    comments = Comment.objects.filter(post=post)
    for com in comments:
        if not Notification.objects.filter(
            Q(user=com.post.author) & Q(message=f"Новый комментарий: {com.text}")
        ).exists():
            Notification.objects.create(
                user=com.post.author,
                sender=user,
                sender_name=sender_name,
                message=f"Новый комментарий: {com.text}",
                is_new=True,
            )


def is_favorite_post(user: User, post: Post) -> bool:
    """
    Проверяет, является ли пост избранным для пользователя.

    args:
            user (User): Пользователь.
            post (Post): Пост.

    return:
            bool: True, если пост является избранным, иначе False.
    """
    return post.favorite_set.filter(user=user).exists()


def create_post_for_user(request) -> PostForm:
    """
    Обрабатывает форму создания поста и создает новый пост для пользователя.

    args:
            request: HTTP запрос.

    return:
            PostForm: Форма поста.
    """
    form = PostForm(request.POST)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.for_subscribers = request.POST.get("for_subscribers", False) == "on"
        post.save()
        form.save_m2m()
        _create_post_notifications(post, request.user)
    return form


def _create_post_notifications(post, user: User):
    """
    Создает уведомления для подписчиков автора поста о новом посте.

    args:
            post (Post): Новый пост.
            user (User): Автор поста.
    """
    post_detail_url = reverse("post_detail", args=[post.id])
    subscribers = Subscription.objects.filter(author=user)
    for subscriber in subscribers:
        Notification.objects.create(
            user=subscriber.subscriber,
            sender=user,
            sender_name=user.username,
            message=f"Новый пост: <a href='{post_detail_url}'>{post.title}</a>",
            is_new=True,
        )


def get_user_posts(user: User) -> QuerySet[Post]:
    """
    Получает посты пользователя, отсортированные по дате публикации.

    args:
            user (User): Пользователь.

    return:
            QuerySet[Post]: QuerySet постов пользователя.
    """
    return Post.objects.filter(author=user).order_by("-publish_date")


def get_all_categories() -> QuerySet[Category]:
    """
    Получает все категории.

    return:
            QuerySet[Category]: QuerySet категорий.
    """
    return Category.objects.all()


def get_post_by_id(pk: int) -> Post:
    """
    Получает пост по его идентификатору.

    args:
            pk (int): Идентификатор поста.

    return:
            Post: Пост.
    """
    return get_object_or_404(Post, pk=pk)


def check_user_permission_to_edit_post(user: User, post: Post) -> None:
    """
    Проверяет, имеет ли пользователь право редактировать пост.

    args:
            user (User): Пользователь.
            post (Post): Пост.

    raises:
            Http404: Если пользователь не имеет прав на редактирование поста.
    """
    if user != post.author:
        raise Http404("Вы не имеете прав на редактирование данного поста")


def handle_edit_post_form(request, post: Post) -> PostForm:
    """
    Обрабатывает форму редактирования поста.

    args:
            request: HTTP запрос.
            post (Post): Пост для редактирования.

    return:
            PostForm: Форма поста.
    """
    form = PostForm(request.POST, instance=post)
    if form.is_valid():
        post = form.save(commit=False)
        post.for_subscribers = (
            request.POST.get("for_subscribers") == "on"
            if request.POST.get("for_subscribers")
            else False
        )
        post.save()
        form.save_m2m()
    return form


def get_post_edit_context(post: Post) -> Dict[str, Any]:
    """
    Формирует контекст данных для редактирования поста.

    args:
            post (Post): Пост.

    return:
            Dict[str, Any]: Контекст данных.
    """
    return {
        "categories": Category.objects.all(),
        "selected_categories": post.categories.all(),
        "for_subscribers": post.for_subscribers,
    }


def get_category_by_slug(category_slug: str) -> Category:
    """
    Получает категорию по её слагу.

    args:
            category_slug (str): Слаг категории.

    return:
            Category: Категория.
    """
    return get_object_or_404(Category, slug=category_slug)


def get_posts_by_category(category: Category, user: User) -> QuerySet[Post]:
    """
    Получает посты по категории с учетом подписки пользователя.

    args:
            category (Category): Категория.
            user (User): Пользователь.

    return:
            QuerySet[Post]: QuerySet постов.
    """
    posts = Post.objects.filter(categories=category).order_by("-publish_date")
    if user.is_authenticated:
        subscribed_authors = user.subscriptions.values_list("author__id", flat=True)
        posts = posts.filter(
            Q(for_subscribers=False)
            | Q(author__id__in=subscribed_authors)
            | Q(author=user)
        )
    else:
        posts = posts.filter(for_subscribers=False)
    return posts


def get_posts_by_query(query: str, user: User) -> QuerySet[Post]:
    """
    Получает посты по запросу с учетом подписки пользователя.

    args:
            query (str): Поисковый запрос.
            user (User): Пользователь.

    return:
            QuerySet[Post]: QuerySet постов.
    """
    if query:
        posts = (
            Post.objects.filter(
                Q(title__icontains=query)
                | Q(body__icontains=query)
                | Q(author__username__icontains=query)
            )
            .distinct()
            .order_by("-publish_date")
        )
    else:
        posts = Post.objects.all().order_by("-publish_date")

    if user.is_authenticated:
        subscribed_authors = user.subscriptions.values_list("author__id", flat=True)
        posts = posts.filter(
            Q(for_subscribers=False)
            | Q(author__id__in=subscribed_authors)
            | Q(author=user)
        )
    else:
        posts = posts.filter(for_subscribers=False)

    return posts


def get_paginated_posts(request, posts: QuerySet[Post]) -> Dict[str, Any]:
    """
    Получает пагинированные посты.

    args:
            request: HTTP запрос.
            posts (QuerySet[Post]): QuerySet постов.

    return:
            Dict[str, Any]: Пагинированные посты.
    """
    posts = posts.order_by("-publish_date")
    paginator = GeneralPaginator(posts)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return {"page_obj": page_obj}


def toggle_post_like(post_id: int, user: User) -> None:
    """
    Переключает лайк поста пользователем.

    args:
            post_id (int): Идентификатор поста.
            user (User): Пользователь.
    """
    post = get_object_or_404(Post, pk=post_id)
    if user in post.likes.all():
        post.likes.remove(user)
    else:
        post.likes.add(user)


def get_subscribed_posts(
    user: User, query: str = None, page_number: str = None
) -> Dict[str, Any]:
    """
    Получает посты подписанных авторов.

    args:
            user (User): Пользователь.
            query (str, optional): Поисковый запрос.
            page_number (str, optional): Номер страницы для пагинации.

    return:
            Dict[str, Any]: Пагинированные посты и подписчики авторов.
    """
    subscriptions = Subscription.objects.filter(subscriber=user)
    subscribed_authors = [subscription.author for subscription in subscriptions]
    all_posts = []
    for author in subscribed_authors:
        author_posts = Post.objects.filter(author=author)
        if query:
            author_posts = author_posts.filter(
                Q(title__icontains=query)
                | Q(body__icontains=query)
                | Q(author__username__icontains=query)
            )
        all_posts.extend(author_posts)

    all_posts_sorted = sorted(all_posts, key=lambda x: x.publish_date, reverse=True)

    paginator = GeneralPaginator(all_posts_sorted)
    page_obj = paginator.get_page(page_number)

    author_subscribers = {}
    if user.is_authenticated:
        authors = {post.author_id: post.author for post in page_obj.object_list}
        author_subscribers = {
            author_id: list(
                User.objects.filter(subscriptions__subscriber=user, id=author_id)
            )
            for author_id in authors.keys()
        }

    return {
        "page_obj": page_obj,
        "author_subscribers": author_subscribers,
    }


def toggle_favorite_post(post_id: int, user: User) -> None:
    """
    Переключает избранный статус поста пользователем.

    args:
            post_id (int): Идентификатор поста.
            user (User): Пользователь.
    """
    post = Post.objects.get(pk=post_id)
    favorite, created = Favorite.objects.get_or_create(user=user, post=post)
    if not created:
        favorite.delete()


def get_favorite_posts(user: User, page_number: str = None) -> Dict[str, Any]:
    """
    Получает избранные посты пользователя.

    args:
            user (User): Пользователь.
            page_number (str, optional): Номер страницы для пагинации.

    return:
            Dict[str, Any]: Пагинированные избранные посты.
    """
    favorite_posts = Favorite.objects.filter(user=user).select_related("post")
    paginator = GeneralPaginator(favorite_posts)
    page_obj = paginator.get_page(page_number)

    return {"page_obj": page_obj}
