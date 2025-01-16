# backend/mavericks/models.py
from django.db import models
from django.contrib.auth.models import User

class Maverick(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mavericks') 
    name = models.CharField(max_length=255)  # Name of the Maverick
    bio = models.TextField(blank=True, null=True)  # Optional bio for the Maverick
    profile_picture = models.ImageField(upload_to='mavericks/', null=True, blank=True)  # Optional image
    location = models.CharField(max_length=255, blank=True, null=True)  # Optional location
    created_at = models.DateTimeField(auto_now_add=True)  # When the Maverick was created

    def __str__(self):
        return self.name
