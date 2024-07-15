from .models import Notification

def unread_notifications_count(request):
    if request.user.is_authenticated:
        unread_count = Notification.objects.filter(user=request.user, is_read=False).count()
        unread_notifications = Notification.objects.filter(user=request.user, is_read=False).order_by('-timestamp')
        return {'unread_notifications_count': unread_count, 'unread_notifications': unread_notifications}
    return {'unread_notifications_count': 0, 'unread_notifications': []}
