from django.shortcuts import render, redirect
from products.models import Product, Category, Review
from products.forms import ProductCreateForm, ReviewCreateForm
from products.constatns import PAGINTION_LIMIT

# Create your views here.


def main_view(request):
    return render(request, 'layouts/index.html')


def product_view(request):
    if request.method == 'GET':
        category_id = int(request.GET.get('category_id', 0))
        search = request.GET.get('search')
        page = int(request.GET.get('page', 1))

        if category_id:
            product = Product.objects.filter(categories__in=[category_id])
        else:
            product = Product.objects.all()

        max_page = product.__len__() / PAGINTION_LIMIT

        if round(max_page) < max_page:
            max_page = round(max_page) + 1

        max_page = int(max_page)
        product = product[PAGINTION_LIMIT * (page-1):PAGINTION_LIMIT * page]

        if search:
            product = product.filter(title__icontains=search)

        return render(request, 'products/products.html', context={
            'products': product,
            'user': None if request.user.is_anonymous else request.user,
            'max_page': range(1, max_page+1)
        })


def products_detail_view(request, id):
    if request.method == 'GET':
        product = Product.objects.get(id=id)

        context = {
            'products': product,
            'reviews': product.reviews.all(),
            'categories': product.categories.all(),
            'review_form': ReviewCreateForm
        }

        return render(request, 'products/detail.html', context=context)

    if request.method == "POST":
        product = Product.objects.get(id=id)
        form = ReviewCreateForm(data=request.POST)

        if form.is_valid():
            Review.objects.create(
                author=request.user,
                post_id=id,
                text=form.cleaned_data.get('text')
            )
            return redirect(f'/products/{id}/')
        else:
            return render(request, 'products/detail.html', context={
                'products': product,
                'reviews': product.reviews.all(),
                'categories': product.categories.all(),
                'review_form': form
            })


def categories_view(request):
    if request.method == "GET":
        categories = Category.objects.all()

        context = {
            'categories': categories
        }

        return render(request, 'categories/index.html', context=context)


def products_create_view(request):
    if request.method == "GET":
        return render(request, 'products/create.html', context={
            'form': ProductCreateForm
        })

    if request.method == "POST":
        form = ProductCreateForm(data=request.POST)

        if form.is_valid():
            Product.objects.create(
                author=request.user,
                title=form.cleaned_data.get('title'),
                description=form.cleaned_data.get('description'),
                rate=form.cleaned_data.get('rate', 0),
                reviewtable=form.cleaned_data.get('reviewtable', True)
            )

            return redirect('/products/')
        else:
            return render(request, 'products/create.html', context={
                'form': form
            })
