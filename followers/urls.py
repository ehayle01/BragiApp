# followers/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('follow/<int:user_id>/', views.follow_user, name='follow_user'),
    path('unfollow/<int:user_id>/', views.unfollow_user, name='unfollow_user'),

    # paths for followers and following lists
    path('followers/<str:username>/', views.followers_list, name='followers_list'),
    path('following/<str:username>/', views.following_list, name='following_list'),
]
