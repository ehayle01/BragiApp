# backend/toolbar/views.py
from django.shortcuts import render
from .models import ToolbarItem, ToolbarAd, UsersItem, UserChildItem

def manage_toolbar(request):
    toolbar_ad = ToolbarAd.objects.first()  
    toolbar_items = ToolbarItem.objects.filter(visible=True)  

    toolbar_user_items = UsersItem.objects.filter(visible=True)
    user_child_items = UserChildItem.objects.filter(visible=True)



    return render(request, 'toolbar/manage_toolbar.html', {
        'toolbar_items': toolbar_items,
        'toolbar_ad': toolbar_ad,
        'toolbar_user_items': toolbar_user_items,  # Adjusted variable name
        'user_child_items': user_child_items,
    })