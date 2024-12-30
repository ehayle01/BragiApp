# toolbar/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('manage/', views.manage_toolbar, name='manage_toolbar'),  # Optional
]
