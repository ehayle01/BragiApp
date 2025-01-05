# followers/models.py
from django.db import models
from django.conf import settings

class Follow(models.Model):
    follower = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        related_name='following', 
        on_delete=models.CASCADE
    )
    followed = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        related_name='followers', 
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'followed')  # Ensure a user can't follow the same user multiple times

    def __str__(self):
        return f"{self.follower.username} follows {self.followed.username}"
