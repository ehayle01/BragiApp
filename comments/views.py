# comments/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from posts.models import Post
from .models import Comment
from .forms import CommentForm

@login_required
def create_comment(request, post_id, parent_id=None):
    post = Post.objects.get(id=post_id)  # Get the post
    parent_comment = None
    
    # If it's a reply, get the parent comment
    if parent_id:
        parent_comment = Comment.objects.get(id=parent_id)
    
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            if parent_comment:  # If it's a reply, associate with the parent
                comment.parent = parent_comment
            comment.save()
            return redirect('post_detail', pk=post.id)  # Redirect back to the post detail page
    else:
        form = CommentForm()

    return render(request, 'posts/post_detail.html', {'post': post, 'form': form, 'parent_comment': parent_comment})
