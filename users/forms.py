# backend\users\forms.py
from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']  # Email is visible only to the user

class UserProfileEditForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'profile_picture', 'location']  # Add location field