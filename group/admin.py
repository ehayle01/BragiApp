# backend/groups/admin.py
from django.contrib import admin
from .models import Group
from django.contrib.auth.models import User
from .forms import GroupForm

class GroupAdmin(admin.ModelAdmin):
    form = GroupForm 
    list_display = ('name', 'creator', 'created_at', 'get_members')
    search_fields = ('name', 'description', 'creator__username')
    list_filter = ('created_at',)
    filter_horizontal = ('members',)
    ordering = ('-created_at',)

    def get_members(self, obj):
        return ", ".join([member.username for member in obj.members.all()])
    get_members.short_description = 'Members'

    # Custom permission check for adding groups
    def has_add_permission(self, request):
        # Only users with the "can_add_group" permission can add groups
        return request.user.has_perm('groups.can_add_group')

    # Custom permission check for changing groups
    def has_change_permission(self, request, obj=None):
        # Only users with the "can_edit_group" permission can edit groups
        return request.user.has_perm('groups.can_edit_group')

    # Custom permission check for deleting groups
    def has_delete_permission(self, request, obj=None):
        # Only users with the "can_delete_group" permission can delete groups
        return request.user.has_perm('groups.can_delete_group')

admin.site.register(Group, GroupAdmin)
