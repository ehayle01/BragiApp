#backend\posts\views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from django.contrib.auth.decorators import login_required
from .forms import PostForm, PostEditForm, CommentForm, CommentEditForm
from django.contrib.auth.models import User
from django.db.models import Q
from fuzzywuzzy import fuzz
from django.http import Http404



def post_list(request):
    query = request.GET.get('q')  # Get the search query from the URL parameter

    if query:
        # Using fuzzy search for title and content match
        posts = Post.objects.all()
        
        # Search by title, content, and author username with fuzzy matching
        posts = [
            post for post in posts if 
            (fuzz.partial_ratio(post.title.lower(), query.lower()) > 60 or  # Fuzzy matching for title
             fuzz.partial_ratio(post.content.lower(), query.lower()) > 60 or  # Fuzzy matching for content
             fuzz.partial_ratio(post.author.username.lower(), query.lower()) > 60)  # Fuzzy matching for author
        ]

        posts.sort(key=lambda post: max(
            fuzz.partial_ratio(post.title.lower(), query.lower()), 
            fuzz.partial_ratio(post.content.lower(), query.lower()),
            fuzz.partial_ratio(post.author.username.lower(), query.lower())
        ), reverse=True)
    
    else:
        posts = Post.objects.all().order_by('-created_at')

    return render(request, 'posts/post_list.html', {
        'posts': posts,
        'current_user': request.user,
        'query': query  # Pass the query to the template to pre-fill the search box
    })


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.filter(parent=None).order_by('-created_at')  # Get top-level comments

    # Handling comment form submission (including replies)
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        parent_comment = None
        if 'parent_comment_id' in request.POST:
            parent_comment = get_object_or_404(Comment, pk=request.POST['parent_comment_id'])
        if comment_form.is_valid():
            comment_form.save(commit=False, parent=parent_comment)
            comment_form.instance.post = post
            comment_form.instance.author = request.user
            comment_form.save()
            return redirect('post_detail', pk=post.pk)
    else:
        comment_form = CommentForm()

    return render(request, 'posts/post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
    })


def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)  # Handle both form data and uploaded files
        if form.is_valid():
            form.instance.author = request.user  # Ensure the logged-in user is the author
            form.save()
            return redirect('post_list')  # Redirect after creating the post
    else:
        form = PostForm()

    return render(request, 'posts/post_form.html', {'form': form})


# Edit Post View
@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # Check if the logged-in user is the author of the post
    if post.author != request.user:
        return redirect('post_list')  # Redirect to the post list if the user is not the author

    if request.method == 'POST':
        form = PostEditForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=post.pk)  # Redirect to the post detail page after saving
    else:
        form = PostEditForm(instance=post)

    return render(request, 'posts/post_edit.html', {'form': form, 'post': post})


# Comment Edit View
@login_required
def comment_edit(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    # Ensure the logged-in user is the author of the comment
    if comment.author != request.user:
        raise Http404("You are not authorized to edit this comment.")

    if request.method == 'POST':
        # Handle form submission for editing the comment
        content = request.POST.get('content')

        if content.strip():
            comment.content = content
            comment.save()

            # Return a JSON response with the updated content
            return JsonResponse({'success': True, 'content': comment.content})

        return JsonResponse({'success': False, 'error': 'Comment content cannot be empty.'})

    return redirect('post_detail', pk=comment.post.pk)


# Delete Comment View
@login_required
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    # Ensure the user is the author of the comment
    if comment.author != request.user:
        raise Http404("You are not authorized to delete this comment.")

    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', pk=post_pk)


