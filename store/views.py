from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from main.models import NewProducts, ContactInfo


def product_list(request, template_name):
    sort_by = request.GET.get('sort', 'default')
    products = NewProducts.objects.all()
    contact_info = ContactInfo.objects.first()

    if sort_by == "cheap":
        products = products.order_by('main_price')
    elif sort_by == "expensive":
        products = products.order_by('-main_price')

    context = {
        'products': products,
        'contact_info': contact_info
    }

    print("Products count:", products.count())
    return render(request, template_name, context)


def main_view(request, template_name):
    product_item_new = NewProducts.objects.all()

    context = {
        'product_item': product_item_new,
    }
    return render(request, template_name, context)


class ProductDetailView(DetailView):
    model = NewProducts
    template_name = 'main/product-page.html'
    context_object_name = 'product'
