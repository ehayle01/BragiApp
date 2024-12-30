# backend/toolbar/admin.py
from django.contrib import admin
from .models import ToolbarItem, Toolbar

@admin.register(ToolbarItem)
class ToolbarItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'subtext', 'url', 'order', 'visible')

@admin.register(Toolbar)
class ToolbarAdmin(admin.ModelAdmin):
    list_display = ('name', 'alt_text', 'url', 'image', 'visible')  # Show the external image in the admin panel
