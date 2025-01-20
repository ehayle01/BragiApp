#BragiApp\maverick\urls.py
from django.urls import path
from users import views as user_views
from . import views

urlpatterns = [
    # Route to create a new Maverick
    path('create/', views.create_maverick, name='create_maverick'),

    # Route to view a Maverick's public profile
    path('maverick/<int:id>/', views.maverick_profile, name='maverick_profile'),

    # Route to edit a Maverick's profile (only accessible by the owner)
    path('maverick/edit/<int:id>/', views.edit_maverick_profile, name='edit_maverick_profile'),

    path('maverick/', views.list_mavericks, name='list_mavericks'), # users maverick list
    path('<int:id>/delete/', views.delete_maverick, name='delete_maverick'),  # Add delete URL

    path('mavericks/', views.mixed_listing, name='mixed_listing'),  # Mixed listing of Mavericks and users
    path('profile/<str:username>/', user_views.public_profile_view, name='public_profile_view'),  # User profile view



]
