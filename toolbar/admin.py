from django.contrib import admin
from .models import ToolbarItem, ToolbarAd

# Inline admin for ToolbarItem, only displaying child items for a parent ToolbarItem
class ToolbarItemInline(admin.TabularInline):
    model = ToolbarItem
    extra = 1  # How many empty child items to show by default
    fields = ('name', 'subtext', 'url', 'order', 'visible')  # Customize which fields to display for the child items
    fk_name = 'parent'  # We link child items to their parent

    def get_queryset(self, request):
        """
        Only show child items (those with a parent) when editing a parent ToolbarItem.
        """
        # If we have an instance (we are editing a specific item)
        if 'object_id' in request.resolver_match.kwargs:
            parent_id = request.resolver_match.kwargs['object_id']
            return ToolbarItem.objects.filter(parent_id=parent_id)
        return ToolbarItem.objects.none()

@admin.register(ToolbarItem)
class ToolbarItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'subtext', 'url', 'order', 'visible')
    list_filter = ('parent',)  # Allows filtering by parent in the admin list
    search_fields = ('name', 'url')  # Allow searching by name or URL
    list_display_links = ('name',)  # Makes the name clickable
    inlines = [ToolbarItemInline]  # Display child ToolbarItems for a given parent in the same form

@admin.register(ToolbarAd)
class ToolbarAdAdmin(admin.ModelAdmin):
    list_display = ('name', 'alt_text', 'url', 'image', 'visible')
    # No inline for ToolbarItem here, only manage the Toolbar itself
