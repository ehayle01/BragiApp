# backend/groups/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import GroupCreateForm
from .models import Group


@login_required
def create_group(request):
    if request.method == 'POST':
        form = GroupCreateForm(request.POST, request.FILES)  # Ensure you include request.FILES here
        if form.is_valid():
            group = form.save(commit=False)  # Create group without saving to DB yet
            group.creator = request.user  # Set the current logged-in user as the creator of the group
            group.save()  # Save the group object to the database

            # Now, manually save the many-to-many relationship (members)
            members = form.cleaned_data.get('members')  # Get selected members from cleaned data
            group.members.set(members)  # Save members to the group (many-to-many relationship)

            # Add the creator as a member
            group.members.add(group.creator)  # Add creator to the members list automatically
            
            return redirect('group_detail', group_id=group.id)  # Redirect to the group detail page
    else:
        form = GroupCreateForm()

    return render(request, 'group/create_group.html', {'form': form})



@login_required
def group_detail(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    return render(request, 'group/group_detail.html', {'group': group})


@login_required
def group_list(request):
    groups = Group.objects.all()  # Retrieve all groups
    return render(request, 'group/group_list.html', {'groups': groups})


@login_required
def edit_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    
    # Check if the current user is the creator of the group
    if group.creator != request.user:
        return redirect('group_detail', group_id=group.id)  # Redirect to group details if not the creator
    
    if request.method == 'POST':
        form = GroupCreateForm(request.POST, request.FILES, instance=group)  # Include request.FILES here
        if form.is_valid():
            group = form.save()  # Save the edited group

            # Ensure the creator is still a member after editing (just in case they were removed)
            group.members.add(group.creator)
            
            return redirect('group_detail', group_id=group.id)  # Redirect to the group detail page after editing
    else:
        form = GroupCreateForm(instance=group)  # Pre-fill the form with the group's current data

    return render(request, 'group/edit_group.html', {'form': form, 'group': group})




@login_required
def user_groups(request):
    # Filter groups by members that contain the current logged-in user
    groups = Group.objects.filter(members=request.user)
    return render(request, 'group/user_groups.html', {'groups': groups})
