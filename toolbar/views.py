# backend/toolbar/views.py

from django.shortcuts import render
from .models import ToolbarItem, Toolbar

def manage_toolbar(request):
    toolbar_items = ToolbarItem.objects.filter(parent__isnull=True)  # Top-level items
    toolbar = Toolbar.objects.first()  # Get the first (or only) toolbar
    return render(request, 'toolbar/manage_toolbar.html', {'toolbar_items': toolbar_items, 'toolbar': toolbar})
