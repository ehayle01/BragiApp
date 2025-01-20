# BragiApp\posts\views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Post
from django.contrib.auth.decorators import login_required
from .forms import PostForm, PostEditForm
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import Http404, JsonResponse
from comments.models import Comment
from filters.models import Category, Tag



@login_required
def post_list(request):
    categories = Category.objects.all()
    tags = Tag.objects.all()
    
    # Retrieve filters from GET request
    category_filter = request.GET.get('category')
    tag_filter = request.GET.get('tag')
    query = request.GET.get('q') 
    
    # Initialize the queryset for published posts
    posts = Post.objects.filter(status='published').prefetch_related('like_set')

    # Apply category filter if provided
    if category_filter:
        posts = posts.filter(category__id=category_filter)

    # Apply tag filter if provided
    if tag_filter:
        posts = posts.filter(tags__id=tag_filter)

    # If there is a search query, perform fuzzy search on the title, content, and author
    if query:
        posts = posts.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query) | 
            Q(author__username__icontains=query)
        )

    # Pass the context for rendering
    context = {
        'posts': posts,
        'current_user': request.user,
        'query': query,  # Pre-fill the search box
        'categories': categories,
        'tags': tags,
        'category_filter': category_filter,
        'tag_filter': tag_filter,
    }

    return render(request, 'posts/post_list.html', context)



# View for displaying post details
@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # Only increment view count if the user has not viewed this post in this session
    if not request.session.get(f'viewed_post_{post.pk}', False):
        post.views += 1
        post.save()
        request.session[f'viewed_post_{post.pk}'] = True

    # Ensure comments are ordered by 'created_at' in descending order
    comments = Comment.objects.filter(post=post, parent__isnull=True).order_by('-created_at')

    # Pass the Maverick to the template if the post has a Maverick linked
    maverick = post.maverick if post.maverick else None

    return render(request, 'posts/post_detail.html', {
        'post': post,
        'comments': comments,  # Passing top-level comments to the template
        'maverick': maverick,  # Passing the Maverick if present
    })


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, user=request.user)  # Pass the user to the form
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # Set the author before saving

            # If a Maverick is selected, it will be saved with the post
            post.maverick = form.cleaned_data.get('maverick')

            if 'publish' in request.POST:  # Check if the publish button was clicked
                post.status = 'published'  # Set post status as published
            else:
                post.status = 'draft'  # Otherwise, save as draft

            post.save()

            # Redirect depending on whether the post is published or still a draft
            if post.status == 'published':
                return redirect('post_detail', pk=post.pk)  # Redirect to post detail if published
            else:
                return redirect('draft_posts')  # Redirect to drafts list if saved as draft
        else:
            print(form.errors)  # Log form errors for debugging
    else:
        form = PostForm(user=request.user)  # Pass user to the form

    return render(request, 'posts/post_form.html', {'form': form})


# For editing a post (post_edit view)
@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # Ensure the logged-in user is the author of the post
    if post.author != request.user:
        return redirect('post_list')  # Redirect to the post list if the user is not the author

    if request.method == 'POST':
        form = PostEditForm(request.POST, request.FILES, instance=post)  # No need to pass user here
        if form.is_valid():
            # Check if the user clicked "Publish" or "Save Changes"
            post = form.save(commit=False)
            if 'publish' in request.POST:
                post.status = 'published'  # Mark as published
            else:
                post.status = 'draft'  # Keep as draft

            post.save()  # Save the post with the updated status

            # After saving, redirect to either the post detail or back to drafts
            if post.status == 'published':
                return redirect('post_detail', pk=post.pk)  # Redirect to post detail if published
            else:
                return redirect('draft_posts')  # Redirect back to draft posts if saved as draft

        else:
            print(form.errors)  # Log form errors for debugging
    else:
        form = PostEditForm(instance=post)

    return render(request, 'posts/post_edit.html', {'form': form, 'post': post})


@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # Ensure that the logged-in user is the author of the post
    if post.author != request.user:
        raise Http404("You do not have permission to delete this post")

    if request.method == 'POST':
        post.delete()  # Delete the post
        messages.success(request, 'Your post has been deleted successfully.')  # Add a success message
        return redirect('post_list')  # Redirect to the post list page after deletion

    return render(request, 'posts/delete_confirm.html', {'post': post})


@login_required
def draft_posts(request):
    drafts = Post.objects.filter(author=request.user, status='draft')  # Filter drafts for the logged-in user
    return render(request, 'posts/draft_list.html', {'drafts': drafts})
