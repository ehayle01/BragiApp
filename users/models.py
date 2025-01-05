#backend\users\models.py
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)  # Bio field
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)  # Profile picture
    location = models.CharField(max_length=255, blank=True, null=True)  # New location field


    def __str__(self):
        return f"Profile of {self.user.username}"

