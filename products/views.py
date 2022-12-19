from django.shortcuts import render
from products.models import Product


# Create your views here.


def main_view(request):
    return render(request, 'layouts/index.html')


def product_view(request):
    if request.method == 'GET':
        product = Product.objects.all()

        return render(request, 'products/products.html', context={
            'products': product
        })


def products_detail_view(request, id):
    if request.method == 'GET':
        product = Product.objects.get(id=id)

        context = {
            'products': product,
            'reviews': product.reviews.all()
        }

        return render(request, 'products/detail.html', context=context)
