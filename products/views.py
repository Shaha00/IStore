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
