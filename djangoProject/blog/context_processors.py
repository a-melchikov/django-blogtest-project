from .models import Notification

def notifications_count(request):
    if request.user.is_authenticated:
        count = Notification.objects.filter(user=request.user, viewed=False).count()
    else:
        count = 0
    return {'notifications_count': count}