# backend/toolbar/context_processors.py
from .models import ToolbarItem, Toolbar

def toolbar_items(request):
    return {
        'toolbar_items': ToolbarItem.objects.filter(visible=True),
        'toolbar': Toolbar.objects.filter(visible=True).first(),  # Get the first (or only) visible toolbar
    }