from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages  # Import messages
from .forms import ProfileForm

@login_required
def profile_view(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            # Add a success message
            messages.success(request, 'Your profile information has been saved successfully!')
            return redirect('profiles')  # Redirect to the profile page (or another page)
    else:
        form = ProfileForm(instance=profile)
    
    return render(request, 'profiles/profiles.html', {'form': form})
