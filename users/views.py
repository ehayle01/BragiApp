 #users/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required  
from django.contrib.auth.models import User
from posts.models import Post  
from .forms import UserEditForm, UserProfileEditForm
from .models import UserProfile 
from followers.models import Follow


# Public Profile View (for viewing any user's profile)
def public_profile_view(request, username):
    # Get the user by username
    user = get_object_or_404(User, username=username)  
    
    # Retrieve the associated profile of the user
    user_profile, created = UserProfile.objects.get_or_create(user=user)
    
    # Retrieve posts created by this user
    user_posts = Post.objects.filter(author=user).order_by('-created_at')
    
    # Check if the current user is logged in
    is_authenticated = request.user.is_authenticated
    
    # Check if the logged-in user is following the user whose profile is being viewed
    is_following = False
    if is_authenticated:
        # Check if a Follow relationship exists
        is_following = Follow.objects.filter(follower=request.user, followed=user).exists()

    # Get the count of followers and following
    followers_count = Follow.objects.filter(followed=user).count()  # Count of people following this user
    following_count = Follow.objects.filter(follower=user).count()  # Count of users that this user is following

    # Pass the context to the template
    return render(request, 'users/public_profile.html', {
        'user': user,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'is_authenticated': is_authenticated,
        'is_following': is_following,  # Include this to check if the user is following
        'followers_count': followers_count,  # Number of followers
        'following_count': following_count,  # Number of people the user is following
    })


# Register View
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user to the database
            
            # Create the UserProfile for the new user
            UserProfile.objects.create(user=user)  # Automatically create the profile
            
            login(request, user)  # Log the user in immediately after registration
            return redirect('profile')  # Redirect to the profile page after registration
    else:
        form = UserCreationForm()  # If GET request, show an empty form

    return render(request, 'registration/register.html', {'form': form})  # Render the registration template




# Profile View (requires the user to be logged in)
@login_required
def profile_view(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    # Retrieve posts that the logged-in user has created
    user_posts = Post.objects.filter(author=request.user).order_by('-created_at')

    # Get the count of followers and following for the logged-in user
    followers_count = Follow.objects.filter(followed=request.user).count()  # Count of people following the user
    following_count = Follow.objects.filter(follower=request.user).count()  # Count of users the user is following

    # Create links for followers and following list pages
    followers_url = f"/followers/followers/{request.user.username}/"
    following_url = f"/followers/following/{request.user.username}/"

    return render(request, 'users/profile.html', {
        'user': request.user,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'followers_count': followers_count,
        'following_count': following_count,
        'followers_url': followers_url,  # Pass the followers list URL
        'following_url': following_url,  # Pass the following list URL
    })

@login_required
def profile_edit_view(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=request.user)
        profile_form = UserProfileEditForm(request.POST, request.FILES, instance=user_profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()  # Save the user data
            profile_form.save()  # Save the profile data
            print(f"Profile updated: {user_profile}")  # Debugging line
            return redirect('profile')  # Redirect to the profile view after saving
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = UserProfileEditForm(instance=user_profile)

    return render(request, 'users/profile_edit.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })
