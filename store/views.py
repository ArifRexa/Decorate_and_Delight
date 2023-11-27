from django.shortcuts import render
from .models import Products, Category, Subcategory
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.


# ========================================= Jewellery ===========================================
def jewellery_view(request):
    categories = Category.objects.all()
    subcategories = Subcategory.objects.all()
    products = Products.objects.filter(category__name='Jewellery')

    # Apply filters based on request parameters
    category_filter = request.GET.get('category')
    subcategory_filter = request.GET.get('subcategory')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    ratings = request.GET.getlist('ratings')
    star_ratings = [i for i in range(1, 6)]

    if category_filter:
        products = products.filter(category__name=category_filter)

    if subcategory_filter:
        products = products.filter(subcategory__name=subcategory_filter)

    if min_price and max_price:
        products = products.filter(price__range=(min_price, max_price))

    rating_filter = request.GET.get('rating')
    if rating_filter:
        products = products.filter(ratings__gte=float(rating_filter))

    # Pagination
    page = request.GET.get('page')
    paginator = Paginator(products, 2)  # Change the number based on your preference
    try:
        paginated_products = paginator.page(page)
    except PageNotAnInteger:
        paginated_products = paginator.page(1)
    except EmptyPage:
        paginated_products = paginator.page(paginator.num_pages)

    context = {
        'products': paginated_products,
        'categories': categories,
        'subcategories': subcategories,
        'star_ratings': star_ratings,
    }
    return render(request, 'jewellery/jewellery.html', context)


def jewellery_details_view(request, product_id):
    product = Products.objects.get(id=product_id)
    star_ratings = [i for i in range(1, 6)]
    context = {
        'product': product,
        'star_ratings': star_ratings,
    }
    return render(request, 'jewellery/details.html', context)


# ========================================= Bed Sheet ===========================================

def bedsheet_view(request):
    # jewelry_category_id = 1
    # jewelries = Products.objects.all()
    bedsheets = Products.objects.filter(category_id=2)
    return render(request, 'bedsheet/bedsheet.html', {'bedsheets': bedsheets})


def bedsheet_details_view(request, product_id):
    product = Products.objects.get(id=product_id)
    return render(request, 'bedsheet/details.html', {'product': product})
