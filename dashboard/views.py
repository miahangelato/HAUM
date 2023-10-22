from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy

from core.forms import SignupForm
from dashboard.forms import EditUserForm
from item.models import Item
from profile.forms import UserUpdateForm
from profile.models import Profile


# Create your views here.
@login_required
def index_d(request):
    items = Item.objects.filter(created_by=request.user)
    users = User.objects.all()
    user_id = request.user.id

    return render(request, 'dashboard/index_d.html', {
        'item': items,
        'user_id': user_id,
        'users': users
    })

def add_user(request):
    user = request.user
    if user.is_superuser:
        if request.method == 'POST':
            form = SignupForm(request.POST)
            if form.is_valid():
                user = form.save()
                user.is_active = True
                user.save()
                return redirect('dashboard:index_d')

        else:
            form = SignupForm()

        return render(request, 'core/signup.html', {'form': form})


def delete_user(request, user_id):
    if request.user.is_superuser:
        try:
            user_to_delete = User.objects.get(pk=user_id)
            user_to_delete.delete()
            return redirect('dashboard:index_d')
        except User.DoesNotExist:
            raise Http404("User does not exist")
    else:
        raise Http404("Permission denied")

def edit_user(request, user_id):
    print(user_id)
    instance = User.objects.get(pk=user_id)
    if request.user.is_superuser:
        user = get_object_or_404(Profile, user=instance)
        print(user)
        if request.method == 'POST':

            form = EditUserForm(request.POST, instance=user)
            user_form = UserUpdateForm(request.POST, instance=instance)
            if form.is_valid() and user_form.is_valid():
                user = form.save()
                user.is_active = True
                user.save()
                user_form.save()
                return redirect('dashboard:index_d')

        else:
            form = EditUserForm(instance=user)
            user_form = UserUpdateForm(instance=instance)
            context = {
                'form': form,
                'user_form': user_form,
            }
        return render(request, 'dashboard/edit_user.html', context)
    else:
        raise Http404("Permission denied")



