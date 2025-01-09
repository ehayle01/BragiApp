# backend/groups/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import GroupCreateForm
from .models import Group


@login_required
def create_group(request):
    if request.method == 'POST':
        form = GroupCreateForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)  # Create group without saving to DB yet
            group.creator = request.user  # Set the current logged-in user as the creator of the group
            group.save()  # Save the group object to the database

            # Now, manually save the many-to-many relationship (members)
            members = form.cleaned_data.get('members')  # Get selected members from cleaned data
            group.members.set(members)  # Save members to the group (many-to-many relationship)
            
            # Redirect to the group detail page
            return redirect('group_detail', group_id=group.id)
    else:
        form = GroupCreateForm()

    return render(request, 'group/create_group.html', {'form': form})


def group_detail(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    return render(request, 'group/group_detail.html', {'group': group})

def group_list(request):
    groups = Group.objects.all()  # Retrieve all groups
    return render(request, 'group/group_list.html', {'groups': groups})