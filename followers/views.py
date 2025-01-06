# BragiApp\followers\views.py
from django.shortcuts import redirect, get_object_or_404, render
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



def followers_list(request, username):
    user = get_object_or_404(User, username=username)
    
    # Get all users who are following the current user
    followers = Follow.objects.filter(followed=user).select_related('follower')
    
    return render(request, 'followers/followers_list.html', {
        'user': user,
        'followers': followers,
    })

def following_list(request, username):
    user = get_object_or_404(User, username=username)
    
    # Get all users that the current user is following
    following = Follow.objects.filter(follower=user).select_related('followed')
    
    return render(request, 'followers/following_list.html', {
        'user': user,
        'following': following,
    })