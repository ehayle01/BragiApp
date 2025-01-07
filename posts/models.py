#backend\posts\models.py
from django.db import models
from django.contrib.auth.models import User  # Assuming you are using Django's built-in User model
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', default=1)  # Adding an author field
    image = models.ImageField(upload_to='posts/images/', null=True, blank=True)  # Field for image upload (optional)
    file = models.FileField(upload_to='posts/files/', null=True, blank=True)  # Field for file upload (optional)

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='posts')
    tags = models.ManyToManyField(Tag, related_name='posts', blank=True)

    views = models.IntegerField(default=0)  # To track how many times the post is viewed


    def likes(self):
        return self.like_set.all()

    def __str__(self):
        return self.title


