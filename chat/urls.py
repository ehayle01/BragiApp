# BragiApp\chat\urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.communication_center, name='communication_center'),
    path('<int:user_id>/', views.chat_thread, name='chat_thread'),
    path('<int:thread_id>/load_messages/', views.load_messages, name='load_messages'),
    
]