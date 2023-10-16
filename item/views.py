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
from django.db.models import Q, ExpressionWrapper, F, Count, fields
from django.db.models.functions import Now
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy

from item.forms import NewItemForm, EditItemForm
from item.models import Item, Category, PriceRange
from profile.models import Location


def items(request):
    query = request.GET.get('query', '')
    category_ids = request.GET.getlist('categories')  # Get a list of selected category IDs
    location_ids = request.GET.getlist('locations')  # Get a list of selected location IDs
    price_range_ids = request.GET.getlist('price_ranges')  # Get a list of selected price range IDs
    min_price = request.GET.get('min_price', 0)
    max_price = request.GET.get('max_price', float('inf'))

    category = Category.objects.all()
    locations = Location.objects.all()
    items = Item.objects.filter(is_sold=False)
    price_ranges = PriceRange.objects.all()

    upvoted = request.GET.get('upvoted', False)
    downvoted = request.GET.get('downvoted', False)
    most_downvoted = request.GET.get('most_downvoted', False)

    # Annotate the items with upvote and downvote counts
    items = items.annotate(
        upvotes_count=Count('created_by__profile__uservote', filter=Q(created_by__profile__uservote__is_upvote=True)),
        downvotes_count=Count('created_by__profile__uservote', filter=Q(created_by__profile__uservote__is_upvote=False))
    )

    # Calculate the age of the item
    items = items.annotate(age=ExpressionWrapper(Now() - F('created_at'), output_field=fields.DurationField()))

    # To implement "Most Upvoted" sorting with recency:
    if upvoted:
        items = items.order_by('-upvotes_count', 'age')  # Sort by most upvoted items with recency
    elif most_downvoted:
        items = items.order_by('-downvotes_count')  # Sort by most downvoted items
    else:
        items = items.order_by('-upvotes_count')  # Default to sorting by most upvoted items


    if category_ids:
        items = items.filter(category_id__in=category_ids)

    if location_ids:
        items = items.filter(created_by__profile__location_id__in=location_ids)

    if price_range_ids:
        selected_price_ranges = PriceRange.objects.filter(id__in=price_range_ids)
        price_filter = Q()
        for price_range in selected_price_ranges:
            price_filter |= Q(price__gte=price_range.min_price, price__lte=price_range.max_price)
        items = items.filter(price_filter)
    else:
        items = items.filter(price__gte=min_price, price__lte=max_price)

    if query:
        items = items.filter(Q(name__icontains=query) | Q(description__icontains=query))

    return render(request, 'item/items.html', {
        'items': items,
        'query': query,
        'category': category,
        'location': locations,
        'price_ranges': price_ranges,
        'selected_price_ranges': price_range_ids,
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
