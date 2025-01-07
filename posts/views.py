# BragiApp\posts\views.py

from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Category, Tag
from django.contrib.auth.decorators import login_required
from .forms import PostForm, PostEditForm
from django.contrib.auth.models import User
from django.db.models import Q
#from fuzzywuzzy import fuzz
from django.http import Http404, JsonResponse
from comments.models import Comment


# View for listing posts
@login_required
def post_list(request):
    query = request.GET.get('q')  # Get the search query from the URL parameter
    category_filter = request.GET.get('category')  # Get the category filter from the URL
    tag_filter = request.GET.get('tag')  # Get the tag filter from the URL

    posts = Post.objects.prefetch_related('like_set').all()
    
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
@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # Only increment view count if the user has not viewed this post in this session
    if not request.session.get(f'viewed_post_{post.pk}', False):
        post.views += 1
        post.save()
        request.session[f'viewed_post_{post.pk}'] = True

    comments = Comment.objects.filter(post=post, parent__isnull=True)

    return render(request, 'posts/post_detail.html', {
        'post': post,
        'comments': comments,  # Passing top-level comments to the template
    })


# View for creating a new post
@login_required
def post_create(request):
    if request.method == 'POST':
        print("POST request received")  # Add this for debugging
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.author = request.user
            form.save()
            print("Form is valid and post saved")
            return redirect('post_list')
        else:
            print(form.errors)  # Log form errors if validation fails
    else:
        form = PostForm()
    return render(request, 'posts/post_form.html', {'form': form})



@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # Ensure the logged-in user is the author of the post
    if post.author != request.user:
        return redirect('post_list')  # Redirect to the post list if the user is not the author

    if request.method == 'POST':
        form = PostEditForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            post.refresh_from_db()  # Refresh post to ensure it's updated
            return redirect('post_detail', pk=post.pk)  # Redirect to the post detail page after saving
        else:
            # Log form errors to help with debugging
            print(form.errors)  # Check the server console for errors
    else:
        form = PostEditForm(instance=post)

    return render(request, 'posts/post_edit.html', {'form': form, 'post': post})