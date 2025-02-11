#backend\posts\models.py
from django.db import models
from django.contrib.auth.models import User  # Assuming you are using Django's built-in User model
from django.utils import timezone
from maverick.models import Maverick  # Import the Maverick model
from filters.models import Category, Tag

class Post(models.Model):
    DRAFT = 'draft'
    PUBLISHED = 'published'

    POST_STATUS_CHOICES = [
        (DRAFT, 'Draft'),
        (PUBLISHED, 'Published'),
    ]

    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', default=1)

    maverick = models.ForeignKey(Maverick, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts')  # Optional Maverick field
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    
    image = models.ImageField(upload_to='posts/images/', null=True, blank=True)
    file = models.FileField(upload_to='posts/files/', null=True, blank=True)
    views = models.IntegerField(default=0)
    status = models.CharField(
        max_length=10,
        choices=POST_STATUS_CHOICES,
        default=DRAFT,  # Default to draft status
    )

    def likes(self):
        return self.like_set.all()

    def __str__(self):
        return self.title

