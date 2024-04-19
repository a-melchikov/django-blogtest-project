from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import Http404, HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from django.views.generic import (
    ListView,
    DetailView,
    TemplateView,
    DeleteView,
)
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User

from authentication.models import Profile

from .models import Category, Message, Notification, Post, Comment
from .forms import PostForm, ProfileForm, CommentForm


class BlogList(ListView):
    model = Post
    template_name = "home.html"
    context_object_name = "posts"
    paginate_by = 5
    ordering = "-publish_date"

    def get_queryset(self):
        return Post.objects.all().order_by(self.ordering)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(context["posts"], self.paginate_by)
        page_number = self.request.GET.get("page")
        try:
            page_obj = paginator.get_page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        context["posts"] = page_obj
        return context


class BlogDetailView(DetailView):
    model = Post
    template_name = "post_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context["comments"] = post.comments.filter(approved_comment=True).order_by(
            "-created_date"
        )
        context["comment_form"] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        post = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            categories = request.POST.getlist("categories")
            if categories:
                post.categories.add(*categories)

            sender_name = request.user.username

            user = request.user
            comments = Comment.objects.filter(post__author=user)
            comments = Comment.objects.filter(post=post)
            for com in comments:
                if not Notification.objects.filter(
                    Q(user=com.post.author)
                    & Q(message=f"Новый комментарий: {com.text}")
                ).exists():
                    Notification.objects.create(
                        user=com.post.author,
                        sender_name=sender_name,
                        message=f"Новый комментарий: {com.text}",
                        is_new=True,
                    )
            return HttpResponseRedirect(reverse("post_detail", args=[post.pk]))
        else:
            return self.render_to_response(self.get_context_data(form=form))


class AboutPageView(TemplateView):
    template_name = "about.html"


@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            return redirect("home")
    else:
        form = PostForm()
    return render(request, "create_post.html", {"form": form})


@login_required
def my_posts(request):
    # Получаем все посты текущего пользователя
    user = request.user
    user_posts = Post.objects.filter(author=user).order_by("-publish_date")
    return render(request, "my_posts.html", {"user_posts": user_posts})


@login_required
def edit_profile(request, user_name):
    user = get_object_or_404(User, username=user_name)

    if request.user != user:
        raise Http404("Вы не имеете прав на редактирование данного профиля")

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect("user_profile", user_name=request.user.username)
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, "edit_profile.html", {"form": form})


@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.user != post.author:
        raise Http404("Вы не имеете прав на редактирование данного поста")

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect("my_posts")
    else:
        form = PostForm(instance=post)

    selected_categories = post.categories.all()

    categories = Category.objects.all()
    return render(
        request,
        "edit_post.html",
        {
            "form": form,
            "categories": categories,
            "selected_categories": selected_categories,
        },
    )


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy(
        "my_posts"
    )  # После успешного удаления перенаправить на страницу с моими постами
    template_name = (
        "post_confirm_delete.html"  # Создайте шаблон подтверждения удаления поста
    )


@login_required
def inbox(request):
    messages = Message.objects.filter(recipient=request.user).order_by("-timestamp")
    return render(request, "inbox.html", {"messages": messages})


@login_required
def send_message(request):
    if request.method == "POST":
        recipient = request.POST["recipient"]
        subject = request.POST["subject"]
        body = request.POST["body"]

        sender = request.user

        message = Message(
            sender=sender,
            recipient=Profile.objects.get(user__username=recipient).user,
            subject=subject,
            body=body,
        )
        message.save()

        sender_name = sender.username
        Notification.objects.create(
            user=message.recipient,
            sender=sender,
            sender_name=sender_name,
            message=f"Новое сообщение: {message.subject}",
            is_new=True,
        )

        return redirect("inbox")
    else:
        profiles = Profile.objects.all()
        return render(request, "send_message.html", {"profiles": profiles})


@login_required
def user_profile_view(request, user_name):
    # Получаем пользователя по его имени или возвращаем 404 ошибку, если пользователь не найден
    user = get_object_or_404(User, username=user_name)
    user_posts = Post.objects.filter(author=user).order_by("-publish_date")
    # Здесь можно передать данные о пользователе и его постах в шаблон для отображения
    return render(request, "profile.html", {"user": user, "user_posts": user_posts})


class AllProfilesView(ListView):
    model = Profile
    template_name = "all_profiles.html"
    context_object_name = "profile_list"

    def get_queryset(self):
        return Profile.objects.all()


@login_required
def notifications(request):
    user = request.user
    not_viewed_count = Notification.objects.filter(user=user, viewed=False).count()
    notif = Notification.objects.filter(user=user, is_new=True)[::-1]

    for notification in notif:
        notification.type, notification.text = str(notification).split(":")

    if request.method == "POST":
        notification_ids = request.POST.getlist("notification_ids")
        Notification.objects.filter(id__in=notification_ids).update(viewed=True)
        return redirect("notifications")

    return render(
        request,
        "notifications.html",
        {"notifications": notif, "notifications_count": not_viewed_count},
    )


def category_posts(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    posts = Post.objects.filter(categories=category).order_by("-publish_date")
    context = {
        "category": category,
        "posts": posts,
    }
    return render(request, "category_posts.html", context)


def search_posts(request):
    query = request.GET.get("query")
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
    return render(request, "search_results.html", {"posts": posts})


@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    user = request.user
    if request.method == "POST":
        if user in post.likes.all():
            post.likes.remove(user)
        else:
            post.likes.add(user)
    return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))


@login_required
def delete_notification(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id)
    if request.user == notification.user:
        notification.delete()
        messages.success(request, 'Уведомление успешно удалено.')
        return redirect('notifications')
    else:
        return HttpResponseForbidden("Вы не имеете прав на удаление этого уведомления.")
