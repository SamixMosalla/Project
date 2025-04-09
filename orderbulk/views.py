from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.shortcuts import render, redirect
from .forms import BulkOrderForm


def bulk_order_view(request):
    if request.method == 'POST':
        form = BulkOrderForm(request.POST)
        if form.is_valid():
            order = form.save()

            subject = 'سفارش عمده جدید'
            from_email = settings.DEFAULT_FROM_EMAIL  
            to_email = 'receiver@example.com' 

            text_content = f"""\
نام: {order.first_name}
نام خانوادگی: {order.last_name}
شماره تماس: {order.phone}
واتساپ: {order.whatsapp}
ایمیل: {order.email}
مقدار سفارش: {order.amount_kg} کیلوگرم
"""

            html_content = f"""\
<html>

<body>
    <table width="100%" cellpadding="0" cellspacing="0" border="0"
        style="font-family: Arial, Tahoma, sans-serif;  padding: 20px; direction: rtl; ">
        <tr>
            <td align="center">
                <table width="600" cellpadding="20" cellspacing="0" border="0"
                    style="background-color: #ffffff; border-radius: 8px; direction: rtl; text-align: right; box-shadow: 0px 2px 4px 0px rgba(0, 0, 0, 0.1); padding: 20px; font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;">
                    <tr>
                        <td style="color: #4CAF50; font-size: 24px; font-weight: bold; text-align: right;">
                            📦 سفارش عمده جدید
                        </td>
                    </tr>
                    <tr>
                        <td style="color: #333333; font-size: 16px; padding: 10px 0; text-align: right;">
                            <strong style="display: inline-block; width: 120px;">نام:</strong> {order.first_name}
                        </td>
                    </tr>
                    <tr>
                        <td style="color: #333333; font-size: 16px; padding: 10px 0; text-align: right;">
                            <strong style="display: inline-block; width: 120px;">نام خانوادگی:</strong>
                            {order.last_name}
                        </td>
                    </tr>
                    <tr>
                        <td style="color: #333333; font-size: 16px; padding: 10px 0; text-align: right;">
                            <strong style="display: inline-block; width: 120px;">شماره تماس:</strong> {order.phone}
                        </td>
                    </tr>
                    <tr>
                        <td style="color: #333333; font-size: 16px; padding: 10px 0; text-align: right;">
                            <strong style="display: inline-block; width: 120px;">واتساپ:</strong> {order.whatsapp}
                        </td>
                    </tr>
                    <tr>
                        <td style="color: #333333; font-size: 16px; padding: 10px 0; text-align: right;">
                            <strong style="display: inline-block; width: 120px;">ایمیل:</strong> {order.email}
                        </td>
                    </tr>
                    <tr>
                        <td style="color: #333333; font-size: 16px; padding: 10px 0; text-align: right;">
                            <strong style="display: inline-block; width: 120px;">مقدار سفارش:</strong> {order.amount_kg}
                            کیلوگرم
                        </td>
                    </tr>
                    <tr>
                        <td style="color: #333333; font-size: 16px; padding: 10px 0; text-align: right;">
                            <p style="display: inline-block; width: 100%; text-align: left;"> :) Created By Hashashin Group
                            </p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>

</html>
"""
            msg = EmailMultiAlternatives(
                subject, text_content, from_email, [to_email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            return redirect('main:index')
    else:
        form = BulkOrderForm()

    return render(request, 'orderbulk/orderblukform.html', {'form': form})
