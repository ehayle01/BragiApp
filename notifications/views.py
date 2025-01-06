from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Notification

@login_required
def notifications_list(request):
    # Get all notifications for the logged-in user
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    
    # Mark notifications as read
    if request.GET.get('mark_read'):
        notification_id = request.GET.get('mark_read')
        notification = Notification.objects.get(id=notification_id)
        notification.is_read = True
        notification.save()
    
    return render(request, 'notifications/notifications_list.html', {'notifications': notifications})
