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
    if request.method == 'GET' and 'categories[]' in request.GET:
        category_ids = request.GET.getlist('categories[]')
        products = NewProducts.objects.filter(category__id__in=category_ids)

        products_data = []
        for product in products:
            products_data.append({
                'id': product.id,
                'name': product.name,
                'image_url': product.image.url if product.image else '',
                'short_description': product.Short_description,
                'discount_price': product.discount_price,
                # اطمینان حاصل می‌کنیم که قیمت ارسال می‌شود.
                'main_price': product.main_price,
                'url': product.get_absolute_url(),
                # این لینک رو می‌تونید بسته به نیاز تغییر بدید.
                'cart_url': reverse('main:cart'),
                'bulk_url': reverse('orderbulk:orderbulk'),  # لینک خرید عمده
            })

        return JsonResponse({'products': products_data})
    return JsonResponse({'error': 'Invalid request'}, status=400)


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
