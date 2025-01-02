from django.shortcuts import get_object_or_404, redirect
from posts.models import Post
from .models import Like

def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user.is_authenticated:
        # Check if the user already liked the post
        like = Like.objects.filter(user=request.user, post=post).first()
        if like:
            like.delete()  # Unlike the post
        else:
            Like.objects.create(user=request.user, post=post)  # Like the post
    return redirect('post_detail', pk=post.pk)
