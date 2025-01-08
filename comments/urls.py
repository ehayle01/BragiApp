#BragiApp\comments\urls.py
from django.urls import path
from . import views

urlpatterns = [
    # URL for creating a new comment (with optional parent_id for replies)
    path('create/<int:post_id>/', views.create_comment, name='create_comment'),
    path('create/<int:post_id>/reply/<int:parent_id>/', views.create_comment, name='create_comment_reply'),

    # New URLs for editing and deleting comments
    path('edit/<int:comment_id>/', views.edit_comment, name='edit_comment'),
    path('delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('create_comment/<int:post_id>/<int:parent_id>/', views.create_comment, name='create_comment'),

]
