# backend/posts/views.py

from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment, Category, Tag
from django.contrib.auth.decorators import login_required
from .forms import PostForm, PostEditForm, CommentForm
from django.contrib.auth.models import User
from django.db.models import Q
from fuzzywuzzy import fuzz
from django.http import Http404, JsonResponse


# View for listing posts
def post_list(request):
    query = request.GET.get('q')  # Get the search query from the URL parameter
    category_filter = request.GET.get('category')  # Get the category filter from the URL
    tag_filter = request.GET.get('tag')  # Get the tag filter from the URL

    posts = Post.objects.all()  # Start with all posts, then filter based on search or category/tag
    
    # If there is a search query, perform fuzzy search on the title, content, and author
    if query:
        posts = posts.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query) | 
            Q(author__username__icontains=query)
        )

    # Filter by category if provided
    if category_filter:
        posts = posts.filter(category__name__icontains=category_filter)

    # Filter by tag if provided
    if tag_filter:
        posts = posts.filter(tags__name__icontains=tag_filter)

    # Get all categories and tags to populate filters in the template
    categories = Category.objects.all()
    tags = Tag.objects.all()

    return render(request, 'posts/post_list.html', {
        'posts': posts,
        'current_user': request.user,
        'query': query,  # Pre-fill the search box
        'categories': categories,  # Pass categories for filtering
        'tags': tags,  # Pass tags for filtering
    })


# View for displaying post details
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


# View for creating a new post
@login_required
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


# View for editing a post
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
