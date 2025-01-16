#BragiApp\maverick\views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Maverick
from .forms import MaverickForm
from django.contrib.auth.decorators import login_required
from django.http import Http404

# View to create a new Maverick
@login_required
def create_maverick(request):
    if request.method == 'POST':
        form = MaverickForm(request.POST, request.FILES)
        if form.is_valid():
            maverick = form.save(commit=False)
            maverick.user = request.user  # Assign the currently logged-in user to the Maverick
            maverick.save()
            return redirect('maverick_profile', id=maverick.id)  # Redirect to the newly created Maverick's profile
    else:
        form = MaverickForm()

    return render(request, 'maverick/create_maverick.html', {'form': form})


# View to show a public Maverick profile
def maverick_profile(request, id):
    maverick = get_object_or_404(Maverick, id=id)

    return render(request, 'maverick/maverick_profile.html', {
        'maverick': maverick,
    })

# View to edit a Maverick's profile (only for the owner)
@login_required
def edit_maverick_profile(request, id):
    maverick = get_object_or_404(Maverick, id=id)

    # Ensure that the logged-in user is the owner of the Maverick
    if maverick.user != request.user:
        raise Http404  # Return 404 if the user isn't the owner

    if request.method == 'POST':
        form = MaverickForm(request.POST, request.FILES, instance=maverick)
        if form.is_valid():
            form.save()
            return redirect('maverick_profile', id=maverick.id)  # Redirect to the Maverick profile page
    else:
        form = MaverickForm(instance=maverick)

    return render(request, 'maverick/edit_maverick_profile.html', {'form': form, 'maverick': maverick})