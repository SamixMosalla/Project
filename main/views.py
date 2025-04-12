from .models import NewProducts, ContactInfo, Comment
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Category, NewProducts, NewWeBlog, CartItem, Cart, ProductComment, BillingInfo
from django.http import JsonResponse
from blog.forms import SubscriberForm
from .forms import ContactForm, CommentForm, ProductCommentForm, BillingInfoForm
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth import logout
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
import json
from django.views.decorators.http import require_POST

def index(request):
    return render(request, 'main/index.html')


def about(request):
    return render(request, 'main/about.html')


def contact_view(request):
    contact_info = ContactInfo.objects.first()
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            send_mail(
                subject='پیام جدید از فرم تماس',
                message=f"نام: {form.cleaned_data['name']}\nایمیل: {form.cleaned_data['email']}\n\n{form.cleaned_data['message']}",
                from_email='noreply@example.com',  # ایمیل فرستنده
                recipient_list=['mrahimy1029@gmail.com'],  # ایمیل مدیر سایت
                fail_silently=False
            )
            form.save()
            messages.success(request, 'پیام شما با موفقیت ارسال شد.')
            form = ContactForm()

        else:
            messages.error(request, 'خطایی رخ داد. لطفاً مجدد تلاش کنید.')
    context = {
        'form': form,
        'contact_info': contact_info,
    }
    return render(request, 'main/contact.html', context)


def product_page(request):
    return render(request, 'main/product-page.html')


def main_view(request, template_name):
    category_item = Category.objects.all()
    product_item_new = NewProducts.objects.all().order_by('-created_at')[:4]
    blog_item = NewWeBlog.objects.all().order_by('-time')[:3]
    # product_item = NewProducts.objects.all()
    contact_info = ContactInfo.objects.first()

    context = {
        'category_item': category_item,
        'product_item': product_item_new,
        'blog_item': blog_item,
        # 'all_product': product_item,
        'contact_info': contact_info,
    }

    return render(request, template_name, context)


class ProductDetailView(DetailView):
    model = NewProducts
    template_name = 'main/product-page.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        product_item = NewProducts.objects.all().order_by('-created_at')[:4]

        contact_info = ContactInfo.objects.first()

        comments = ProductComment.objects.filter(
            product=self.object, approved=True)

        form = ProductCommentForm()

        context.update({
            'product_item': product_item,
            'contact_info': contact_info,
            'comments': comments,
            'form': form
        })
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data()

        form = ProductCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = self.object
            comment.save()
            # return redirect('product_detail', pk=self.object.pk)

        context['form'] = form
        return self.render_to_response(context)


class BlogDetailView(DetailView):
    model = NewWeBlog
    template_name = 'main/content.html'
    context_object_name = 'blog'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blog_item'] = NewWeBlog.objects.all().order_by('-time')[:3]
        contact_info = ContactInfo.objects.first()
        context['contact_info'] = contact_info
        context['form'] = SubscriberForm()
        context['comment_form'] = CommentForm()

        context['comments'] = Comment.objects.filter(
            blog=self.object, approved=True)

        if 'name' in self.request.COOKIES:
            context['comment_form'].fields['name'].initial = self.request.COOKIES['name']
        if 'email' in self.request.COOKIES:
            context['comment_form'].fields['email'].initial = self.request.COOKIES['email']

        context['message'] = ''
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)

        subscriber_form = SubscriberForm(request.POST)
        if subscriber_form.is_valid():
            subscriber_form.save()
            context['message'] = "ایمیل شما با موفقیت ثبت شد"
        else:
            context['message'] = ''

        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.blog = self.object
            comment.save()

            response = redirect(self.request.path)
            if comment_form.cleaned_data.get('save_info'):
                response.set_cookie(
                    'name', comment_form.cleaned_data['name'], max_age=365*24*60*60)
                response.set_cookie(
                    'email', comment_form.cleaned_data['email'], max_age=365*24*60*60)
            return response

        context['comment_form'] = comment_form
        context['form'] = subscriber_form
        return self.render_to_response(context)

@require_POST  # این دکوراتور تضمین می‌کند فقط درخواست‌های POST پذیرفته شوند
def add_to_cart(request):
    try:
        # بررسی نوع محتوای درخواست
        content_type = request.headers.get('Content-Type', '')
        
        if 'application/json' in content_type:
            # پردازش درخواست JSON
            data = json.loads(request.body)
            product_id = data.get('product_id')
        else:
            # پردازش درخواست فرم معمولی
            product_id = request.POST.get('product_id')
        
        # اعتبارسنجی product_id
        if not product_id:
            return JsonResponse(
                {"error": "شناسه محصول الزامی است"}, 
                status=400
            )
        
        try:
            product_id = int(product_id)  # تبدیل به عدد برای امنیت بیشتر
        except (ValueError, TypeError):
            return JsonResponse(
                {"error": "شناسه محصول نامعتبر است"}, 
                status=400
            )
        
        # دریافت محصول از دیتابیس
        product = get_object_or_404(NewProducts, id=product_id)
        
        # دریافت یا ایجاد سبد خرید
        cart = request.session.get('cart', {})
        
        # به‌روزرسانی سبد خرید
        if str(product_id) in cart:
            cart[str(product_id)]['quantity'] += 1
        else:
            cart[str(product_id)] = {
                'name': product.name,
                'price': float(product.discount_price),  # تبدیل به float برای اطمینان
                'quantity': 1,
                'image': product.image.url if product.image else '',
            }
        
        # ذخیره سبد خرید در سشن
        request.session['cart'] = cart
        request.session.modified = True
        
        # محاسبه جمع‌های سبد خرید
        total_items = sum(item['quantity'] for item in cart.values())
        total_price = sum(item['quantity'] * item['price'] for item in cart.values())
        
        # پاسخ موفقیت‌آمیز
        return JsonResponse({
            'success': True,
            'total_items': total_items,
            'total_price': total_price,
            'message': 'محصول با موفقیت به سبد خرید اضافه شد'
        })
        
    except Exception as e:
        # ثبت خطا برای دیباگ
        print(f"Error in add_to_cart: {str(e)}")
        return JsonResponse(
            {
                'success': False,
                'error': 'خطای سرور در پردازش درخواست',
                'detail': str(e)
            },
            status=500
        )

def cart_view(request):
    cart = request.session.get("cart", {})
    contact_info = ContactInfo.objects.first()

    for key, product in cart.items():
        product["total_price"] = product["quantity"] * product["price"]

    context = {
        'cart': cart,
        'contact_info': contact_info
    }
    return render(request, "main/cart.html", context)


def remove_from_cart(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        cart = request.session.get("cart", {})

        if product_id in cart:
            del cart[product_id]
            request.session["cart"] = cart
            request.session.modified = True
            return JsonResponse({"success": True})

    return JsonResponse({"error": "Invalid request"}, status=400)


def update_cart(request):
    if request.method == "POST":
        cart = request.session.get("cart", {})

        action = request.POST.get("action")
        product_id = request.POST.get("product_id")

        if product_id not in cart:
            return JsonResponse({"error": "محصول در سبد خرید یافت نشد"}, status=404)

        if action == "remove":
            del cart[product_id]

        elif action == "update":
            new_quantity = int(request.POST.get("quantity", 1))
            cart[product_id]["quantity"] = max(1, new_quantity)

        request.session["cart"] = cart
        request.session.modified = True

        total_items = sum(item["quantity"] for item in cart.values())
        total_price = sum(item["quantity"] * item["price"]
                          for item in cart.values())

        updated_cart = {}
        for product_id, product in cart.items():
            updated_cart[product_id] = {
                "name": product["name"],
                "quantity": product["quantity"],
                "price": product["price"],
                "total_price": product["quantity"] * product["price"]
            }

        return JsonResponse({
            "success": True,
            "total_items": total_items,
            "total_price": total_price,
            "cart": updated_cart
        })

    return JsonResponse({"error": "درخواست نامعتبر است"}, status=400)


def user_logout(request):
    logout(request)
    return redirect('main:index')


def checkout_view(request):
    cart = request.session.get("cart", {})
    contact_info = ContactInfo.objects.first()

    for key, product in cart.items():
        product["total_price"] = product["quantity"] * product["price"]

    if request.method == 'POST':
        form = BillingInfoForm(request.POST)

        if form.is_valid():
            billing_info = form.save(commit=False)

            products_info = ""
            total_price = 0

            for key, item in cart.items():
                products_info += f"""<tr>
                    <td style="padding: 10px; text-align: right;">{item['name']}</td>
                    <td style="padding: 10px; text-align: center;">{item['quantity']}</td>
                    <td style="padding: 10px; text-align: left;">{item['price']} تومان</td>
                </tr>"""
                total_price += item['quantity'] * item['price']

            billing_info.products = products_info
            billing_info.total_price = total_price
            billing_info.save()

            subject = "جزئیات سفارش شما"
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = 'receiver@example.com'

            html_content = f"""\
            <!DOCTYPE html>
            <html lang="fa" dir="rtl">
            <head>
                <meta charset="UTF-8" />
                <title>جزئیات سفارش</title>
            </head>
            <body style="font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif; background-color: #f8f8f8; margin: 0; padding: 20px; direction:rtl;">
                <table align="center" style="max-width: 600px; width: 100%; font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif; background-color: #ffffff; padding: 20px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                    <tr>
                        <td style="text-align: center;">
                            <h2 style="color: #4CAF50; margin-bottom: 5px;">🛒 سفارش جدید ثبت شد!</h2>
                            <p style="color: #666;">اطلاعات سفارش مشتری به شرح زیر است:</p>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <hr style="border: none; border-top: 1px solid #e0e0e0;" />
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <h3 style="color: #333;">👤 اطلاعات مشتری</h3>
                            <p><strong>نام و نام خانوادگی:</strong> {billing_info.first_name} {billing_info.last_name}</p>
                            <p><strong>آدرس:</strong> {billing_info.province}, {billing_info.street}</p>
                            <p><strong>کد پستی:</strong> {billing_info.postal_code}</p>
                            <p><strong>شماره تلفن:</strong> {billing_info.phone_number}</p>
                            <p><strong>ایمیل:</strong> {billing_info.email}</p>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <hr style="border: none; border-top: 1px solid #e0e0e0;" />
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <h3 style="color: #333;">📦 محصولات سفارش‌داده‌شده</h3>
                            <table style="width: 100%; border-collapse: collapse;">
                                <thead>
                                    <tr style="background-color: #f0f0f0;">
                                        <th style="text-align: right; padding: 10px; border-bottom: 1px solid #ddd;">نام محصول</th>
                                        <th style="text-align: center; padding: 10px; border-bottom: 1px solid #ddd;">تعداد</th>
                                        <th style="text-align: left; padding: 10px; border-bottom: 1px solid #ddd;">قیمت</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {products_info}
                                    <tr style="background-color: #f9f9f9;">
                                        <td colspan="2" style="padding: 10px; text-align: left;"><strong>مجموع:</strong></td>
                                        <td style="text-align: left; padding: 10px;"><strong>{total_price} تومان</strong></td>
                                    </tr>
                                </tbody>
                            </table>
                        </td>
                    </tr>
                    <tr>
                        <td style="padding-top: 20px; text-align: center; color: #888;">این ایمیل به صورت خودکار ایجاد شده است. لطفاً به آن پاسخ ندهید.</td>
                    </tr>
                </table>
            </body>
            </html>
            """
            msg = EmailMultiAlternatives(
                subject, html_content, from_email, [to_email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            msg_customer = EmailMultiAlternatives(
                subject, html_content, from_email, [billing_info.email])
            msg_customer.attach_alternative(html_content, "text/html")
            msg_customer.send()

            request.session['cart'] = {}

            return redirect('main:index')

    else:
        form = BillingInfoForm()

    context = {
        'form': form,
        'cart': cart,
        'contact_info': contact_info,
    }

    return render(request, 'main/payment.html', context)
