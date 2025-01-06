from django.db import models
from django.conf import settings
from django.utils import timezone

class Comment(models.Model):
    post = models.ForeignKey('posts.Post', related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Comment by {self.user} on {self.post}'
