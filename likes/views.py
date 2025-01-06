# BragiApp/likes/views.py
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from posts.models import Post
from .models import Like
from notifications.models import Notification


@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # Assuming you want to notify the user who created the post
    user_to_follow = post.author
    
    # Create a notification for the followed user
    Notification.objects.create(
        user=user_to_follow,  # The user who will receive the notification
        message=f'{request.user.username} liked your post.',
        notification_type='like'
    )

    # Check if the user already liked the post
    like = Like.objects.filter(user=request.user, post=post).first()
    if like:
        like.delete()  # Unlike the post
    else:
        Like.objects.create(user=request.user, post=post)  # Like the post

    return redirect('post_detail', pk=post.pk)
