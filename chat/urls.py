# BragiApp\chat\urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.communication_center, name="communication_center"),
    path("<str:thread_name>/", views.chat_thread, name="chat_thread"),
]
