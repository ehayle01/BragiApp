# backend/groups/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from .forms import GroupCreateForm
from .models import Group

@login_required
def create_group(request):
    if request.method == 'POST':
        form = GroupCreateForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.creator = request.user  # Set the creator of the group
            group.save()

            # Add selected members to the group
            form.save_m2m()

            return redirect('group_detail', group_id=group.id)  # Redirect to group details page
    else:
        form = GroupCreateForm()

    return render(request, 'group/create_group.html', {'form': form})


def group_detail(request, group_id):
    group = get_object_or_404(Group, id=group_id)

    return render(request, 'group/group_detail.html', {
        'group': group,
    })