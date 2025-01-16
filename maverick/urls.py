#BragiApp\maverick\urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Route to create a new Maverick
    path('create/', views.create_maverick, name='create_maverick'),

    # Route to view a Maverick's public profile
    path('profile/<int:id>/', views.maverick_profile, name='maverick_profile'),

    # Route to edit a Maverick's profile (only accessible by the owner)
    path('profile/edit/<int:id>/', views.edit_maverick_profile, name='edit_maverick_profile'),
]
