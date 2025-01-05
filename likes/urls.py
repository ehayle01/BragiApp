# BragiApp/likes/urls.py
from django.urls import path
from . import views

app_name = 'likes'  # Add namespace

urlpatterns = [
    path('like/<int:pk>/', views.like_post, name='like_post'),
]
