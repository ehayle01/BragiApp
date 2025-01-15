# backend/groups/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import GroupCreateForm
from .models import Group


@login_required
def create_group(request):
    if request.method == 'POST':
        # Pass the current user to the form via **kwargs
        form = GroupCreateForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            group = form.save(commit=False)
            group.creator = request.user
            group.save()

            members = form.cleaned_data.get('members')
            group.members.set(members)
            group.members.add(group.creator)  # Add creator automatically
            return redirect('group_detail', group_id=group.id)
    else:
        # Pass the current user when creating the form
        form = GroupCreateForm(user=request.user)  # Pass the current user

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
        # Pass the current user to the form and pre-select the current members
        form = GroupCreateForm(request.POST, request.FILES, instance=group, user=request.user)
        if form.is_valid():
            # Save the group details (title, description, location, etc.)
            group = form.save()

            # Get the selected members (including the creator)
            members = form.cleaned_data.get('members')

            # Update the members list
            group.members.set(members)  # Add the new members to the group
            group.members.add(group.creator)  # Ensure the creator remains a member

            return redirect('group_detail', group_id=group.id)  # Redirect to the group detail page after editing
    else:
        # Pass the current user to filter members and pre-select current members
        form = GroupCreateForm(instance=group, user=request.user, initial={'members': group.members.all()})

    return render(request, 'group/edit_group.html', {'form': form, 'group': group})




@login_required
def user_groups(request):
    # Filter groups by members that contain the current logged-in user
    groups = Group.objects.filter(members=request.user)
    return render(request, 'group/user_groups.html', {'groups': groups})
