#BragiApp\posts\urls.py
from django.urls import path, include
from . import views

urlpatterns = [
    # List all posts
    path('', views.post_list, name='post_list'),

    # View a single post's details
    path('post/<int:pk>/', views.post_detail, name='post_detail'),

    # URL for creating a new post
    path('post/new/', views.post_create, name='post_create'),

    # URL for editing a post
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),

    # URL for omments 
    path('post/<int:post_id>/comment/', include('comments.urls')),


    path('likes/', include('likes.urls')),
    
]