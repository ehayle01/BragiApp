 #users/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required  
from django.contrib.auth.models import User
from posts.models import Post  
from .forms import UserEditForm, UserProfileEditForm
from .models import UserProfile 


# Public Profile View (for viewing any user's profile)
def public_profile_view(request, username):
    user = get_object_or_404(User, username=username)  # Get the user by username
    
    # Retrieve the associated profile of the user
    user_profile, created = UserProfile.objects.get_or_create(user=user)

    # Retrieve posts created by this user
    user_posts = Post.objects.filter(author=user).order_by('-created_at')
    # Check if the user is logged in and pass that info to the template
    is_authenticated = request.user.is_authenticated

    return render(request, 'users/public_profile.html', {
        'user': user,
        'user_profile': user_profile,  # Make sure to pass user_profile to the template
        'user_posts': user_posts,
        'is_authenticated': is_authenticated,  # Pass the authentication status

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

    return render(request, 'users/profile.html', {
        'user': request.user,
        'user_profile': user_profile,  # Make sure to pass user_profile to the template
        'user_posts': user_posts,
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
