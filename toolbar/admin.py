#BragiApp\toolbar\admin.py
from django.contrib import admin
from .models import ToolbarItem, ToolbarAd, UserChildItem, UsersItem

@admin.register(ToolbarAd)
class ToolbarAdAdmin(admin.ModelAdmin):
    list_display = ('name', 'alt_text', 'url', 'image', 'visible')
    search_fields = ('name', 'url')  # Search by name or URL


@admin.register(ToolbarItem)
class ToolbarItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'order', 'visible')  # Shows name, URL, order, and visibility in the list view
    search_fields = ('name', 'url')  # Allows searching by name or URL
    list_display_links = ('name',)  # Makes the name clickable

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset


# Inline Model for UserChildItem, displayed inside UsersItem
class UserChildItemInline(admin.TabularInline):
    model = UserChildItem
    extra = 1  # Allows at least one child item by default
    fields = ('icon', 'name', 'url', 'description', 'visible')  # You can customize which fields are displayed here

@admin.register(UsersItem)
class UsersItemAdmin(admin.ModelAdmin):
    inlines = [UserChildItemInline]  # Display UserChildItem inline within UsersItem
    list_display = ( 'name', 'description', 'visible')
    search_fields = ('name', 'description')
    list_display_links = ('name',)
