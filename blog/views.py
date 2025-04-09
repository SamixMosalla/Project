from .models import Subscriber
from .forms import SubscriberForm
from django.shortcuts import render, redirect
from django.shortcuts import render
from main.models import NewWeBlog
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from main.models import ContactInfo


def main_view(request, template_name):
    blog_item = NewWeBlog.objects.all()
    last_blog = blog_item.order_by('-time').first()
    contact_info = ContactInfo.objects.first()

    message = ''
    if request.method == 'POST':
        form = SubscriberForm(request.POST)
        if form.is_valid():
            form.save()
            message = "ایمیل شما با موفقیت ثبت شد"
        else:
            message = ''
    else:
        form = SubscriberForm()

    context = {
        'blog_item': blog_item,
        'last_blog': last_blog,
        'form': form,
        'message': message,
        'contact_info': contact_info,
    }
    return render(request, template_name, context)


def send_newsletter(request):
    subject = "محصول یا مقاله جدید"
    from_email = "your_email@gmail.com"

    subscribers = Subscriber.objects.values_list('email', flat=True)

    if subscribers:
        context = {
            'title': "محصول یا مقاله جدید",
            'body': "یک محصول یا مقاله جدید در سایت منتشر شد. برای مشاهده وارد سایت شوید.",
            'link': 'https://yourwebsite.com',
        }

        html_content = render_to_string(
            'blog/email.html', context)
        text_content = strip_tags(html_content)
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=from_email,
            to=list(subscribers)
        )
        email.attach_alternative(html_content, "text/html")
        email.send()

        msg = "ایمیل‌ها با موفقیت ارسال شدند."
    else:
        msg = "هیچ کاربری در خبرنامه عضو نیست."

    return render(request, 'blog/test.html', {'msg': msg})
