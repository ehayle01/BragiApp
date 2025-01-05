# BragiApp\likes\templatetags\custom_filters.py
from django import template
from likes.models import Like

register = template.Library()

@register.filter(name='has_liked')
def has_liked(post, user):
    if not user.is_authenticated:
        return False
    return Like.objects.filter(post=post, user=user).exists()
