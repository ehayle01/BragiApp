# backend/toolbar/context_processors.py
from .models import ToolbarItem, ToolbarAd

def toolbar_items(request):
    return {
        'toolbar_items': ToolbarItem.objects.filter(visible=True),
        'toolbar_ad': ToolbarAd.objects.filter(visible=True).first(),  # Get the first (or only) visible toolbar
    }