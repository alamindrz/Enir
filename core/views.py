from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import SignupForm
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import ProfileEditForm
from django.shortcuts import render, get_object_or_404
from django.http import Http404


def home(request):
    return render(request, 'home.html')

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Redirect to your home page or any other page
    else:
        form = SignupForm()
    return render(request, 'auth/signup.html', {'form': form})

@login_required
def profile_view(request, user_id):
    # Ensure the logged-in user can only view their own profile
    if request.user.id != user_id:
        raise Http404("You do not have permission to view this profile.")
    
    profile = get_object_or_404(Profile, user__id=user_id)
    return render(request, 'profile/profile.html', {'profile': profile})

@login_required
def edit_profile(request, user_id):
    # Ensure the logged-in user can only edit their own profile
    if request.user.id != user_id:
        raise Http404("You do not have permission to edit this profile.")
    
    profile = get_object_or_404(Profile, user__id=user_id)
    
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('core:profile_view', user_id=user_id)  # Redirect to the profile view page after saving
    else:
        form = ProfileEditForm(instance=profile)
    
    return render(request, 'profile/edit_profile.html', {'form': form})