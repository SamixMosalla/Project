from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from main.models import NewProducts, ContactInfo, Category
from django.template.loader import render_to_string
from django.urls import reverse

# def product_list(request, template_name):
#     sort_by = request.GET.get('sort', 'default')
#     products = NewProducts.objects.all()
#     contact_info = ContactInfo.objects.first()

#     if sort_by == "cheap":
#         products = products.order_by('main_price')
#     elif sort_by == "expensive":
#         products = products.order_by('-main_price')

#     context = {
#         'products': products,
#         'contact_info': contact_info
#     }

#     print("Products count:", products.count())
#     return render(request, template_name, context)


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


def filter_products_ajax(request):
    category_slugs = request.GET.getlist('categories[]')
    if category_slugs:
        products = NewProducts.objects.filter(
            category__slug__in=category_slugs)
    else:
        products = NewProducts.objects.all()

    html = render_to_string('store/store.html', {'products': products})
    return JsonResponse({'html': html})


# def store(request):
#     categories = Category.objects.all()  # همه دسته‌بندی‌ها را می‌گیریم
#     products = NewProducts.objects.all()
#     context = {
#         'categories': categories,
#         'products': products
#     }
#     return render(request, 'store/store.html', context)


# ویو filter_products

def filter_products(request):
    if request.method == 'GET':
        # دریافت دسته‌بندی‌ها به دو روش مختلف (برای سازگاری با هر دو فرمت)
        category_ids = request.GET.getlist('categories[]', []) or request.GET.get('categories', '').split(',')
        
        # حذف مقادیر خالی
        category_ids = [cid for cid in category_ids if cid]
        
        if category_ids:
            try:
                products = NewProducts.objects.filter(category__id__in=category_ids).select_related('category')
            except ValueError:
                return JsonResponse({'error': 'شناسه دسته‌بندی نامعتبر است'}, status=400)
        else:
            # اگر هیچ دسته‌بندی انتخاب نشده، همه محصولات را نمایش بده
            products = NewProducts.objects.all()
        
        products_data = []
        for product in products:
            product_data = {
                'id': product.id,
                'name': product.name,
                'image_url': product.image.url if product.image else '/static/images/no-image.png',
                'short_description': product.Short_description[:100] + '...' if product.Short_description else '',
                'discount_price': int(product.discount_price) if product.discount_price else None,
                'main_price': int(product.main_price) if product.main_price else 0,
                'url': product.get_absolute_url(),
                'cart_url': reverse('main:cart'),
                'bulk_url': reverse('orderbulk:orderbulk'),
                'has_discount': product.discount_price is not None and product.discount_price < product.main_price
            }
            products_data.append(product_data)
        
        return JsonResponse({
            'success': True,
            'products': products_data,
            'count': len(products_data)
        })
    
    return JsonResponse({
        'success': False,
        'error': 'درخواست نامعتبر',
        'message': 'فقط درخواست‌های GET پذیرفته می‌شوند'
    }, status=400)


def store_view(request, template_name='store/store.html'):
    # دریافت دسته‌بندی‌ها
    categories = Category.objects.all()

    # دریافت اطلاعات تماس
    contact_info = ContactInfo.objects.first()

    # دریافت پارامترهای فیلتر و مرتب‌سازی
    selected_categories = request.GET.getlist('categories')
    sort_by = request.GET.get('sort', 'default')

    # فیلتر محصولات بر اساس دسته‌بندی‌های انتخاب شده
    products = NewProducts.objects.all()

    if selected_categories:
        products = products.filter(category__id__in=selected_categories)

    # مرتب‌سازی محصولات
    if sort_by == "cheap":
        products = products.order_by('main_price')
    elif sort_by == "expensive":
        products = products.order_by('-main_price')

    # دیباگ (می‌توانید بعداً حذف کنید)
    print("Categories count:", categories.count())
    print("Products count:", products.count())
    print("Selected categories:", selected_categories)
    print("Sort by:", sort_by)

    context = {
        'categories': categories,
        'products': products,
        'contact_info': contact_info,
        'selected_categories': selected_categories,
        'current_sort': sort_by,
    }

    return render(request, template_name, context)
