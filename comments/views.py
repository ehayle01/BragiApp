# comments/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from posts.models import Post
from .models import Comment
from .forms import CommentForm
from django.contrib.auth.models import User
from notifications.models import Notification

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

            # Create notification message and URL
            if parent_comment:
                # Reply to a comment
                notification_message = f'{request.user.username} replied to your comment.'
                notification_url = f"/post/{post.id}#comment-{comment.id}"

                # Notify the parent comment's author
                Notification.objects.create(
                    user=parent_comment.user,  # Notify the parent comment's author
                    message=notification_message,
                    notification_type='reply',
                    post=post,  # Link notification to post
                    comment=parent_comment  # Link to the parent comment
                )
            else:
                # New comment on the post
                notification_message = f'{request.user.username} commented on your post.'
                notification_url = f"/post/{post.id}"

                # Notify the post's author
                Notification.objects.create(
                    user=post.author,  # Notify the post author
                    message=notification_message,
                    notification_type='comment',
                    post=post,  # Link notification to post
                    comment=comment  # Link notification to the new comment
                )

            return redirect('post_detail', pk=post.id)  # Redirect back to the post detail page
    else:
        form = CommentForm()

    return render(request, 'posts/post_detail.html', {'post': post, 'form': form, 'parent_comment': parent_comment})


@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    
    # Ensure the user is the author of the comment
    if comment.user != request.user:
        return redirect('post_detail', pk=comment.post.id)  # Or a "Permission Denied" page
    
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=comment.post.id)
    else:
        form = CommentForm(instance=comment)

    return render(request, 'comments/edit_comment.html', {'form': form, 'comment': comment})


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    
    # Ensure the user is the author of the comment
    if comment.user != request.user:
        return HttpResponseForbidden("You are not authorized to delete this comment.")

    post_id = comment.post.id
    comment.delete()
    
    return redirect('post_detail', pk=post_id)