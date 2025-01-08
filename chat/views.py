# BragiApp\chat\views.py
from django.shortcuts import render

def communication_center(request):
    return render(request, "chat/communication_center.html")

def chat_thread(request, thread_name):
    return render(request, "chat/chat_thread.html", {"thread_name": thread_name})