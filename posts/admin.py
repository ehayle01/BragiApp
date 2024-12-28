# backend/posts/admin.py
from django.contrib import admin
from .models import Post, Category, Tag


# Register the Post model with customization
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # Columns to display in the list view
    list_display = ('title', 'author', 'created_at', 'updated_at', 'category')  # Added category to list display
    search_fields = ('title', 'content')  # Fields to search by in the admin
    list_filter = ('created_at', 'category')  # Filter posts by created_at and category
    list_display_links = ('title',)  # Make the title clickable in the admin
    fields = ('title', 'content', 'author', 'category', 'tags', 'image', 'file')  # Fields to display in the form

    # Adding more advanced tag management
    filter_horizontal = ('tags',)  # This gives a nice, multi-select interface for tags

    # Add image preview for images uploaded in the admin
    def image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="100" />'
        return 'No Image'
    image_preview.allow_tags = True  # Allow HTML in the admin list view

    # Add the image preview to the list display (optional)
    list_display += ('image_preview',)

# Register the Category and Tag models
admin.site.register(Category)
admin.site.register(Tag)
