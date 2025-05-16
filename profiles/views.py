from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages  # Import messages
from .forms import ProfileForm


from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

from .forms import UserUpdateForm, ProfileImageForm


# @login_required
# def profile_view(request):
#     profile = request.user.profile
#     if request.method == 'POST':
#         form = ProfileForm(request.POST, instance=profile)
#         if form.is_valid():
#             form.save()
#             # Add a success message
#             messages.success(request, 'Your profile information has been saved successfully!')
#             return redirect('profiles')  # Redirect to the profile page (or another page)
#     else:
#         form = ProfileForm(instance=profile)
    
#     return render(request, 'profiles/profiles.html', {'form': form})




@login_required
def profile_view(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Your profile was updated.')
            return redirect('profiles')
    else:
        user_form = UserUpdateForm(instance=request.user)

    password_form = PasswordChangeForm(request.user)
    return render(request, 'profiles/profiles.html', {
        'form': user_form,
        'password_form': password_form
    })

@login_required
def change_profile_image(request):
    if request.method == 'POST':
        form = ProfileImageForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile image updated.')
    return redirect('profiles')

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password successfully changed.')
        else:
            messages.error(request, 'Please correct the error below.')
    return redirect('profiles')
