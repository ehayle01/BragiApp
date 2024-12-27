from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'updated_at')
    search_fields = ('title', 'content')
    list_filter = ('created_at',)
    list_display_links = ('title',)  # Make the title clickable in the admin
    fields = ('title', 'content', 'author', 'image', 'file')  # Add fields to the form in admin
