# toolbar/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('manage/', views.manage_toolbar, name='manage_'),  # Optional
]
