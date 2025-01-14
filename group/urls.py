# backend/groups/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.group_list, name='group_list'),
    path('create/', views.create_group, name='create_group'),
    path('<int:group_id>/', views.group_detail, name='group_detail'),
    path('<int:group_id>/edit/', views.edit_group, name='edit_group'),  # Add this line for edit group
    path('my-groups/', views.user_groups, name='user_groups'),  # New URL for user's groups
]
