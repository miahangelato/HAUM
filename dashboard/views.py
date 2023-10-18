from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy

from item.models import Item


# Create your views here.
@login_required
def index_d(request):
    items = Item.objects.filter(created_by=request.user)

    return render(request, 'dashboard/index_d.html', {
        'item': items,
    })


