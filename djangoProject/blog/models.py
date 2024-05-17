from autoslug import AutoSlugField
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    slug = AutoSlugField(
        populate_from="name", unique=True, null=True, verbose_name="Slug"
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=450, verbose_name="Заголовок")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    body = RichTextField(verbose_name="Текст")
    publish_date = models.DateTimeField(
        default=timezone.now, verbose_name="Дата публикации"
    )
    categories = models.ManyToManyField(Category, verbose_name="Категории")
    likes = models.ManyToManyField(User, related_name="liked_posts", blank=True)
    for_subscribers = models.BooleanField(
        default=False, verbose_name="Только для подписчиков"
    )

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Пост",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор",
    )
    text = models.TextField(verbose_name="Текст комментария")
    created_date = models.DateTimeField(
        default=timezone.now, verbose_name="Дата создания"
    )
    approved_comment = models.BooleanField(default=True, verbose_name="Одобрен")

    def approve(self):
        self.approved_comment = True
        self.save()

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return self.text


class Like(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name="Пост")
    like = models.BooleanField(default=True, verbose_name="Лайк")

    class Meta:
        verbose_name = "Лайк"
        verbose_name_plural = "Лайки"

    def __str__(self):
        return f"{self.user.username} - {self.post.title} - {'Лайк' if self.like else 'Дизлайк'}"


class Favorite(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name="Пост")

    class Meta:
        verbose_name = "Избранное"
        verbose_name_plural = "Избранные посты"
        unique_together = ("user", "post")

    def __str__(self):
        return f"{self.user.username} - {self.post.title}"
