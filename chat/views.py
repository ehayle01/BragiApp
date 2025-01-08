from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import ChatThread
from followers.models import Follow  

@login_required
def communication_center(request):
    # Get the list of users the current user follows
    following = Follow.objects.filter(follower=request.user).select_related('followed')
    return render(request, "chat/communication_center.html", {"following": following})

@login_required
def chat_thread(request, user_id):
    # Get the user to chat with
    other_user = get_object_or_404(User, id=user_id)

    # Ensure the current user follows this user
    if not Follow.objects.filter(follower=request.user, followed=other_user).exists():
        return redirect("communication_center")

    # Check if a thread already exists
    thread, created = ChatThread.objects.get_or_create(
        user1=min(request.user, other_user, key=lambda x: x.id),
        user2=max(request.user, other_user, key=lambda x: x.id)
    )

    # Pass the thread ID and the other user to the template
    return render(request, "chat/chat_thread.html", {"thread_id": thread.id, "other_user": other_user})


