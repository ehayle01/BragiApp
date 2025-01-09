# backend/groups/models.py
from django.db import models
from django.contrib.auth.models import User

class Group(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name='group_members')  # Use a unique related_name
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
