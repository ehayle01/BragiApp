#BragiApp\backend\urls.py
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('posts.urls')),  # This includes all URLs from posts/urls.py
    path('users/', include('users.urls')),  # Include the users app URLs
    path('toolbar/', include('toolbar.urls')),
    path('likes/', include('likes.urls')),
    path('followers/', include('followers.urls')),
    path('notifications/', include('notifications.urls')), 
    path('comments/', include('comments.urls')),
    path("chat/", include("chat.urls")),
    path('groups/', include('group.urls')),
    

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)