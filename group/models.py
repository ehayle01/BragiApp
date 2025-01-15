# backend/groups/models.py
from django.db import models
from django.contrib.auth.models import User

class Group(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name='group_members')
    created_at = models.DateTimeField(auto_now_add=True)

    # New fields:
    cover_image = models.ImageField(upload_to='group_cover_images/', null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        permissions = [
            ("can_add_group", "Can add a new group"),
            ("can_edit_group", "Can edit a group"),
            ("can_delete_group", "Can delete a group"),
        ]

    def __str__(self):
        return self.name