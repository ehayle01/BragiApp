# backend/toolbar/models.py
from django.db import models

class Toolbar(models.Model):  # Separate model for the toolbar's external image
    name = models.CharField(max_length=100, blank=True, null=True)
    alt_text = models.CharField(max_length=200, blank=True, null=True)  # Alt text for the image
    image = models.ImageField(upload_to='toolbar_images/', blank=True, null=True)  # Image upload field
    url = models.URLField(max_length=200, blank=True, null=True)  # Use URLField for link
    visible = models.BooleanField(default=True)

    def __str__(self):
        return "Toolbar"
    

class ToolbarItem(models.Model):
    name = models.CharField(max_length=100)
    subtext = models.CharField(max_length=100, blank=True, null=True)  # Optional field
    url = models.CharField(max_length=200, blank=True, null=True)
    order = models.IntegerField(default=0)
    visible = models.BooleanField(default=True)
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)  # Self-referencing ForeignKey for submenus


    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name