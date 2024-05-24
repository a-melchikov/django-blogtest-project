from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    TemplateView,
    DeleteView,
)
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.mixins import UserPassesTestMixin

from services.paginators import GeneralPaginator
from services.blog_services import (
    get_blog_queryset,
    get_blog_context,
    get_post_comments,
    is_favorite_post,
    handle_comment_form,
    create_post_for_user,
    get_all_categories,
    get_user_posts,
    get_post_by_id,
    check_user_permission_to_edit_post,
    handle_edit_post_form,
    get_post_edit_context,
    get_paginated_posts,
    get_category_by_slug,
    get_posts_by_category,
    get_posts_by_query,
    toggle_post_like,
    get_subscribed_posts,
    toggle_favorite_post,
    get_favorite_posts,
)
from .models import Post
from .forms import PostForm, CommentForm


class BlogList(ListView):
    model = Post
    template_name = "home.html"
    context_object_name = "posts"
    paginate_by = 5
    ordering = "-publish_date"

    def get_queryset(self):
        return get_blog_queryset(self.request.user, self.ordering)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = GeneralPaginator(context["posts"])
        page_number = self.request.GET.get("page")
        context.update(
            get_blog_context(
                self.request.user, context["posts"], paginator, page_number
            )
        )
        return context


class BlogDetailView(UserPassesTestMixin, DetailView):
    model = Post
    template_name = "post/post_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context["comments"] = get_post_comments(post)
        context["comment_form"] = CommentForm()

        user = self.request.user
        if user.is_authenticated:
            context["is_favorite"] = is_favorite_post(user, post)

        return context

    def post(self, request, *args, **kwargs):
        post = self.get_object()

        if not request.user.is_authenticated:
            messages.error(
                request, "Вы должны войти в систему, чтобы оставить комментарий."
            )
            return redirect(reverse("login"))

        form = handle_comment_form(request, post)
        if form.is_valid():
            return HttpResponseRedirect(reverse("post_detail", args=[post.pk]))
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def test_func(self):
        post = self.get_object()
        user = self.request.user
        if not post.for_subscribers:
            return True
        return (post.author == user) or (
            hasattr(user, "subscriptions")
            and user.subscriptions.filter(author=post.author).exists()
        )

    def handle_no_permission(self):
        post = self.get_object()
        return redirect("subscription_confirmation", post_id=post.pk)


class AboutPageView(TemplateView):
    template_name = "about.html"


@login_required
def create_post(request):
    if request.method == "POST":
        form = create_post_for_user(request)
        if form.is_valid():
            return redirect("home")
    else:
        form = PostForm()
    categories = get_all_categories()
    return render(
        request, "post/create_post.html", {"form": form, "categories": categories}
    )


@login_required
def my_posts(request):
    user_posts = get_user_posts(request.user)

    paginator = GeneralPaginator(user_posts)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
    }
    return render(request, "post/my_posts.html", context)


@login_required
def edit_post(request, pk):
    post = get_post_by_id(pk)
    check_user_permission_to_edit_post(request.user, post)

    if request.method == "POST":
        form = handle_edit_post_form(request, post)
        if form.is_valid():
            return redirect("my_posts")
    else:
        form = PostForm(instance=post)

    context = get_post_edit_context(post)
    context.update(
        {
            "form": form,
            "title": post.title,
            "body": post.body,
        }
    )
    print(context)
    return render(
        request,
        "post/edit_post.html",
        context,
    )


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy("my_posts")
    template_name = "post/post_confirm_delete.html"

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author == self.request.user:
            return super().dispatch(request, *args, **kwargs)
        else:
            return get_object_or_404(Post, pk=post.pk)


def category_posts(request, category_slug):
    category = get_category_by_slug(category_slug)
    posts = get_posts_by_category(category, request.user)
    context = {
        "category": category,
        **get_paginated_posts(request, posts),
    }
    return render(request, "post/category_posts.html", context)


def search_posts(request):
    query = request.GET.get("query", "")
    posts = get_posts_by_query(query, request.user)
    context = get_paginated_posts(request, posts)
    return render(request, "search_results.html", context)


@login_required
def like_post(request, pk):
    toggle_post_like(pk, request.user)
    return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))


@login_required
def subscribed_posts(request):
    query = request.GET.get("query", "")
    page_number = request.GET.get("page")
    context = get_subscribed_posts(request.user, query, page_number)
    return render(request, "post/subscribed_posts.html", context)


@login_required
def toggle_favorite(request, post_id):
    toggle_favorite_post(post_id, request.user)
    return redirect("post_detail", pk=post_id)


@login_required
def favorite_posts(request):
    page_number = request.GET.get("page")
    context = get_favorite_posts(request.user, page_number)
    return render(request, "post/favorite_posts.html", context)
