from django.urls import path
from .views import subscribe, SubscriptionConfirmationView, subscriber_list, unsubscribe

urlpatterns = [
    path("subscribe/<int:author_id>/", subscribe, name="subscribe"),
    path("unsubscribe/<int:author_id>/", unsubscribe, name="unsubscribe"),
    path(
        "subscription-confirmation/<int:post_id>/",
        SubscriptionConfirmationView.as_view(),
        name="subscription_confirmation",
    ),
    path("subscribers/<str:username>/", subscriber_list, name="subscriber_list"),
]
