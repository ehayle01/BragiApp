#BragiApp\posts\urls.py
from django.urls import path, include
from . import views

urlpatterns = [
    # List all posts
    path('', views.post_list, name='post_list'),

    # View a single post's details, including comments
    path('post/<int:pk>/', views.post_detail, name='post_detail'),

    # URL for creating a new post
    path('post/new/', views.post_create, name='post_create'),

    # URL for editing a post
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),

    # URL for editing a comment
    path('comment/<int:pk>/edit/', views.comment_edit, name='comment_edit'),
    

    # URL for deleting a comment
    path('comment/<int:pk>/delete/', views.comment_delete, name='comment_delete'),

    path('likes/', include('likes.urls')),
    
]