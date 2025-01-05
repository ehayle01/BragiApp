#BragiApp\likes\models.py
from django.db import models
from django.contrib.auth.models import User
from posts.models import Post

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')  # Ensure a user can only like a post once
        indexes = [
            models.Index(fields=['user', 'post']),  # Optimizes queries
        ]

    def __str__(self):
        return f"{self.user} likes {self.post.title}"
