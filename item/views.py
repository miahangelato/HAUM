# from django.contrib.auth.decorators import login_required
# from django.db.models import Q
# from django.http import HttpResponseRedirect
# from django.shortcuts import render, get_object_or_404, redirect
# from django.urls import reverse_lazy
#
# from item.forms import NewItemForm, EditItemForm
# from item.models import Item, Category, PriceRange
# from profile.models import Location
#
#
# from django.db.models import Q
# from django.shortcuts import render
# from item.models import Item, Category, PriceRange
# from profile.models import Location

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy

from item.forms import NewItemForm, EditItemForm
from item.models import Item, Category, PriceRange
from profile.models import Location


def items(request):
    query = request.GET.get('query', '')
    category_id = request.GET.get('category', 0)
    location_id = request.GET.get('location', 0)
    price_range_id = request.GET.get('price_range', None)
    min_price = request.GET.get('min_price', 0)  # Default to 0 if not provided
    max_price = request.GET.get('max_price', float('inf'))  # Default to infinity if not provided

    category = Category.objects.all()
    locations = Location.objects.all()
    items = Item.objects.filter(is_sold=False)
    price_ranges = PriceRange.objects.all()

    if category_id:
        items = items.filter(category_id=category_id)

    if location_id:
        items = items.filter(created_by__profile__location_id=location_id)

    if price_range_id:
        # Use the selected price range to filter items
        price_range = PriceRange.objects.get(pk=price_range_id)
        items = items.filter(price__gte=price_range.min_price, price__lte=price_range.max_price)
    else:
        # Filter items based on the custom price range provided by the user
        items = items.filter(price__gte=min_price, price__lte=max_price)

    if query:
        items = items.filter(Q(name__icontains=query) | Q(description__icontains=query))

    return render(request, 'item/items.html', {
        'items': items,
        'query': query,
        'category': category,
        'category_id': int(category_id),
        'location': locations,
        'location_id': int(location_id),
        'price_ranges': price_ranges,
        'selected_price_range': int(price_range_id) if price_range_id else None,
        'min_price': min_price,
        'max_price': max_price,
    })





# Create your views here.
def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    related_items = Item.objects.filter(category=item.category, is_sold=False).exclude(pk=item.pk)[0:3]
    context = {
        'item': item,
        'related_items': related_items
    }
    return render(request, 'item/detail.html', context)


@login_required
def NewItem(request):
    if request.method == 'POST':
        form = NewItemForm(request.POST, request.FILES)

        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()

            return redirect('item:detail', pk=item.pk)

    else:
        form = NewItemForm()

    return render(request, 'item/new_item.html', {
        'form': form,
        'title': 'New Item'
    })


@login_required
def delete(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    item.delete()
    return HttpResponseRedirect(reverse_lazy('dashboard:index_d'))

def EditItem(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)

    if request.method == 'POST':
        form = EditItemForm(request.POST, request.FILES, instance=item)

        if form.is_valid():
            form.save()

            return redirect('item:detail', pk=item.pk)

    else:
        form = EditItemForm(instance=item)

    return render(request, 'item/new_item.html', {
        'form': form,
        'title': 'Edit Item'
    })
