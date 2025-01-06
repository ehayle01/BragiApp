from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from posts.models import Post  # Import Post model to associate comment with a post
from .forms import CommentForm  # Import the comment form

@login_required
def create_comment(request, post_id):
    post = Post.objects.get(id=post_id)  # Fetch the post using the post_id
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post  # Associate the comment with the current post
            comment.save()
            return redirect('post_detail', pk=post.id)  # Redirect back to the post details page
    else:
        form = CommentForm()

    return render(request, 'posts/post_detail.html', {'post': post, 'form': form})
