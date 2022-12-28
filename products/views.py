from django.shortcuts import render, redirect
from products.models import Product, Category, Review
from products.forms import ProductCreateForm, ReviewCreateForm


# Create your views here.


def main_view(request):
    return render(request, 'layouts/index.html')


def product_view(request):
    if request.method == 'GET':
        category_id = int(request.GET.get('category_id', 0))

        if category_id:
            product = Product.objects.filter(categories__in=[category_id])
        else:
            product = Product.objects.all()

        return render(request, 'products/products.html', context={
            'products': product
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
                post_id=id,
                text=form.cleaned_data.get('text')
            )
            return redirect(f'/posts/{id}/')
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

    if request.method == "PRODUCT":
        form = ProductCreateForm(data=request.POST)

        if form.is_valid():
            Product.objects.create(
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
