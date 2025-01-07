#BragiApp\notifications\views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Notification

@login_required
def notifications_list(request):
    # Get all notifications for the logged-in user
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    
    # Mark notifications as read if the query param 'mark_read' is passed
    if request.GET.get('mark_read'):
        notification_id = request.GET.get('mark_read')
        try:
            notification = Notification.objects.get(id=notification_id, user=request.user)
            notification.is_read = True
            notification.save()
        except Notification.DoesNotExist:
            pass  # In case the notification doesn't exist
    
    return render(request, 'notifications/notifications_list.html', {'notifications': notifications})
