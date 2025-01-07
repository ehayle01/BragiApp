#BragiApp\notifications\templates\notifications\notifications_list.html
from django.db import models
from django.contrib.auth import get_user_model
from posts.models import Post  # Assuming you have a Post model
from comments.models import Comment  # Assuming you have a Comment model

User = get_user_model()

class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('like', 'Like'),
        ('follow', 'Follow'),
        ('comment', 'Comment'),
        ('reply', 'Reply'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    post = models.ForeignKey(Post, null=True, blank=True, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.notification_type} notification for {self.user.username}'