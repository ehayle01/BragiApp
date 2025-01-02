from django.urls import path
from . import views

urlpatterns = [
    path('like/<int:pk>/', views.like_post, name='like_post'),
]
