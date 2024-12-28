#users/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required  
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from posts.models import Post  
from .forms import UserEditForm

# Public Profile View (for viewing any user's profile)
def public_profile_view(request, username):
    user = get_object_or_404(User, username=username)  # Get the user by username
    
    # Retrieve posts created by this user
    user_posts = Post.objects.filter(author=user).order_by('-created_at')

    return render(request, 'users/public_profile.html', {
        'user': user,
        'user_posts': user_posts
    })

# Register View
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user to the database
            login(request, user)  # Log the user in immediately after registration
            return redirect('profile')  # Redirect to the profile page or other page after registration
    else:
        form = UserCreationForm()  # If GET request, show an empty form

    return render(request, 'registration/register.html', {'form': form})  # Render the registration template


# Profile View (requires the user to be logged in)
@login_required  # Only logged-in users can access the profile
def profile_view(request):
    # Retrieve posts that the logged-in user has created
    user_posts = Post.objects.filter(author=request.user).order_by('-created_at')

    # Pass the posts to the template
    return render(request, 'users/profile.html', {'user': request.user, 'user_posts': user_posts})


@login_required
def profile_edit_view(request):
    # Get the logged-in user's current profile data
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=request.user)  # Pre-populate the form with current user data
        if form.is_valid():
            form.save()  # Save the changes to the user profile
            return redirect('profile')  # Redirect to the profile page after saving changes
    else:
        form = UserEditForm(instance=request.user)  # Initialize the form with the current user data

    return render(request, 'users/profile_edit.html', {'form': form})