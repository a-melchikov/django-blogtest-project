from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=450, verbose_name="Заголовок")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    body = models.TextField(verbose_name="Текст")
    publish_date = models.DateTimeField(
        default=timezone.now, verbose_name="Дата публикации"
    )
    categories = models.ManyToManyField(Category, verbose_name="Категории")

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"

    def __str__(self):
        return self.title


class Message(models.Model):
    sender = models.ForeignKey(
        User,
        related_name="sent_messages",
        on_delete=models.CASCADE,
        verbose_name="Отправитель",
    )
    recipient = models.ForeignKey(
        User,
        related_name="received_messages",
        on_delete=models.CASCADE,
        verbose_name="Получатель",
    )
    subject = models.CharField(max_length=200, verbose_name="Тема")
    body = models.TextField(verbose_name="Текст сообщения")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время")
    read = models.BooleanField(default=False, verbose_name="Прочитано")

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"

    def __str__(self):
        return self.subject


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments",  # Это позволит получить доступ ко всем комментариям определенного поста
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

    # Логика для обработки комментариев (то есть обрабатывать комментарии)
    def approve(self):
        self.approved_comment = True
        self.save()

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return self.text


class Notification(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    message = models.TextField(verbose_name="Сообщение")
    timestamp = models.DateTimeField(default=timezone.now, verbose_name="Дата и время")
    is_new = models.BooleanField(default=True, verbose_name="Новое уведомление")
    viewed = models.BooleanField(default=False, verbose_name="Просмотрено")

    class Meta:
        verbose_name = "Уведомление"
        verbose_name_plural = "Уведомления"

    def __str__(self):
        return self.message
