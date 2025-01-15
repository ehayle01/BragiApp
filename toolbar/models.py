# backend/toolbar/models.py
from django.db import models

class ToolbarAd(models.Model):  # Separate model for the toolbar's external image
    name = models.CharField(max_length=100, blank=True, null=True)
    alt_text = models.CharField(max_length=200, blank=True, null=True)  # Alt text for the image
    image = models.ImageField(upload_to='toolbar_images/', blank=True, null=True)  # Image upload field
    url = models.URLField(max_length=200, blank=True, null=True)  # Use URLField for link
    visible = models.BooleanField(default=True)

    def __str__(self):
        return "Toolbar"
    

class ToolbarItem(models.Model):
    icon = models.FileField(upload_to='toolbar_images/', blank=True, null=True)  # Image upload field
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=200, blank=True, null=True)
    order = models.IntegerField(default=0)
    visible = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name
    


class UsersItem(models.Model):
    
    name = models.CharField(max_length=255)
    icon = models.FileField(upload_to='toolbar_images/', blank=True, null=True)  # Image upload field
    description = models.TextField(blank=True, null=True)
    visible = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class UserChildItem(models.Model):
    list_item = models.ForeignKey(UsersItem, related_name='children', on_delete=models.CASCADE)
    icon = models.FileField(upload_to='toolbar_images/', blank=True, null=True)  # Image upload field
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    visible = models.BooleanField(default=True)

    def __str__(self):
        return self.name