from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required  # Protect views that require login
from posts.models import Post  # Import the Post model to access posts
from .forms import UserEditForm

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