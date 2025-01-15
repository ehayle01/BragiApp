from posts.models import Post  
from toolbar.models import ToolbarItem, ToolbarAd, UsersItem
from group.models import Group


def published_posts_count(request):
    """Return the count of all published posts."""
    count = Post.objects.filter(status='published').count()
    return {'published_posts_count': count}

def toolbar_items(request):
    return {
        'toolbar_items': ToolbarItem.objects.filter(visible=True),
        'toolbar_ad': ToolbarAd.objects.filter(visible=True).first(),  
        'toolbar_user_items': UsersItem.objects.filter(visible=True),  # Plural name for consistency
    }

def group_count(request):
    return {'group_count': Group.objects.count()}