#BragiApp\chat\views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import ChatThread, Message
from followers.models import Follow  
from django.core.paginator import Paginator
from django.http import JsonResponse
from users.models import UserProfile



@login_required
def communication_center(request):
    # Get the list of users the current user follows
    following = Follow.objects.filter(follower=request.user).select_related('followed')

    # Add profile picture URL for each followed user
    for follow in following:
        follow.followed.profile_picture_url = (
            follow.followed.userprofile.profile_picture.url if follow.followed.userprofile.profile_picture else None
        )

    return render(request, "chat/communication_center.html", {"following": following})


@login_required
def chat_thread(request, user_id):
    other_user = get_object_or_404(User, id=user_id)

    if not Follow.objects.filter(follower=request.user, followed=other_user).exists():
        return redirect("communication_center")

    thread, created = ChatThread.objects.get_or_create(
        user1=min(request.user, other_user, key=lambda x: x.id),
        user2=max(request.user, other_user, key=lambda x: x.id)
    )

    # Fetch the latest 20 messages for the thread
    messages = Message.objects.filter(thread=thread).order_by('-timestamp')[:20]
    messages = reversed(messages)  # Display them in ascending order in the template

     # Get profile picture for the other user
    other_user_profile_picture = other_user.userprofile.profile_picture.url if other_user.userprofile.profile_picture else None

    return render(request, "chat/chat_thread.html", {
        "thread_id": thread.id,
        "other_user": other_user,
        "messages": messages,
        "other_user_profile_picture": other_user_profile_picture,
    })


@login_required
def load_messages(request, thread_id):
    thread = get_object_or_404(ChatThread, id=thread_id)
    page = int(request.GET.get('page', 1))

    messages = Message.objects.filter(thread=thread).order_by('-timestamp')
    paginator = Paginator(messages, 20)  # 20 messages per page

    messages_page = paginator.get_page(page)
    messages_data = [
        {"sender": msg.sender.username, "content": msg.content, "timestamp": msg.timestamp.strftime("%H:%M")}
        for msg in messages_page
    ]

    return JsonResponse({"messages": messages_data})