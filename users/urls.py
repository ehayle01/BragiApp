# users/urls.py
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView  # Import LoginView and LogoutView
from django.contrib.auth import views as auth_views
from . import views  # Import custom views (like register_view and profile_view)

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),  # Built-in Login view
    path('register/', views.register_view, name='register'),  # Custom register view
    path('logout/', LogoutView.as_view(), name='logout'),  # Built-in Logout view
    path('profile/', views.profile_view, name='profile'),  # Custom profile view (you need to define this view)
    path('profile/edit/', views.profile_edit_view, name='profile_edit'),  # Profile edit page
    
    path('profile/<str:username>/', views.public_profile_view, name='public_profile'),
    # Password reset URLs
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset_done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),

]