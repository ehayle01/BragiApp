from django import template
from posts.models import Post
from likes.models import Like

register = template.Library()

@register.filter(name='has_liked')
def has_liked(post, user):
    return Like.objects.filter(post=post, user=user).exists()
