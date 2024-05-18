from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import TemplateView

from services.subscription_services import (
    get_user_by_username,
    subscribe_user_to_author,
    unsubscribe_user_from_author,
    get_post_by_id,
    get_user_by_id,
    get_subscriber_profiles,
)


@login_required
def subscribe(request, author_id):
    if request.method == "POST":
        return subscribe_user_to_author(request.user, author_id)
    else:
        author = get_user_by_id(author_id)
        return render(request, "profile/subscribe.html", {"author": author})


@login_required
def unsubscribe(request, author_id):
    if request.method == "POST":
        return unsubscribe_user_from_author(request.user, author_id)
    else:
        author = get_user_by_id(author_id)
        return render(request, "profile/unsubscribe.html", {"author": author})


class SubscriptionConfirmationView(TemplateView):
    template_name = "post/subscription_confirmation.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_id = self.kwargs["post_id"]
        context["post"] = get_post_by_id(post_id)
        context["post_id"] = post_id
        return context


@login_required
def subscriber_list(request, username):
    user = get_user_by_username(username=username)
    subscriber_profiles = get_subscriber_profiles(user)
    return render(
        request,
        "profile/subscriber_list.html",
        {"user": user, "profile_list": subscriber_profiles},
    )
