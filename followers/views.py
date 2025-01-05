# followers/views.py
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Follow
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def follow_user(request, user_id):
    user_to_follow = get_object_or_404(User, id=user_id)
    
    # Prevent the user from following themselves
    if user_to_follow == request.user:
        return redirect('public_profile', username=user_to_follow.username)
    
    # If already following, do nothing
    if Follow.objects.filter(follower=request.user, followed=user_to_follow).exists():
        return redirect('public_profile', username=user_to_follow.username)
    
    # Create follow relationship
    Follow.objects.create(follower=request.user, followed=user_to_follow)
    
    return redirect('public_profile', username=user_to_follow.username)


@login_required
def unfollow_user(request, user_id):
    user_to_unfollow = get_object_or_404(User, id=user_id)
    
    # Check if the user is following the user
    follow = Follow.objects.filter(follower=request.user, followed=user_to_unfollow).first()
    
    if follow:
        follow.delete()  # Remove the follow relationship
    
    return redirect('public_profile', username=user_to_unfollow.username)