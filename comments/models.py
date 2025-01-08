#BragiApp\comments\models.py
from django.db import models
from django.contrib.auth.models import User
from posts.models import Post

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Add this field for nested comments
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.user.username}: {self.content[:20]}'

    class Meta:
        ordering = ['created_at']  # Optional: to order comments by the created_at field