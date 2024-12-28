#backend\users\models.py
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)  # Bio field
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)  # Profile picture

    def __str__(self):
        return f"Profile of {self.user.username}"
