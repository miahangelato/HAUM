from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from item.models import Item
from profile.forms import  UserUpdateForm, ProfileUpdateForm
from profile.models import Profile


@login_required
def profile(request, username):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile', request.user.username)

    else:
        user = User.objects.get(username=username)
        profile = Profile.objects.get(user=user)
        print(user)
        print(profile)
        u_form = UserUpdateForm(instance=user)
        p_form = ProfileUpdateForm(instance=profile)

    is_own_profile = user == request.user

    # Fetch items based on the condition
    if not is_own_profile:
        item = Item.objects.filter(created_by=user)
    else:
        item = None

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'user': user,
        'profile': profile,
        'item': item,
        'is_own_profile': is_own_profile,

    }

    return render(request, 'profile/profile.html', context)



