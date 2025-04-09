from django import forms
from .models import Contact, Comment, ProductComment, BillingInfo


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']
        labels = {
            'name': 'نام خود را وارد کنید .',
            'email': 'ایمیل خود را وارد کنید .',
            'message': 'پیام خود را بنویسید .',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'input-contact mt-3 mb-3',
                'placeholder': 'نام و نام خانوادگی شما',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'input-contact mt-3 mb-3',
                'placeholder': 'پست الکترونیکی شما',
            }),
            'message': forms.Textarea(attrs={
                'class': 'input-contact mt-3 mb-3',
                'placeholder': 'پیام ...',
                'rows': 5,
            }),
        }


class CommentForm(forms.ModelForm):
    save_info = forms.BooleanField(
        required=False, label=' ذخیره نام، ایمیل و وبسایت من در مرورگر برای زمانی که دوباره دیدگاهی می‌نویسم. ')

    class Meta:
        model = Comment
        fields = ['content', 'name', 'email', 'website', 'save_info']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'usercomment mt-2',
            }),

        }


class ProductCommentForm(forms.ModelForm):
    class Meta:
        model = ProductComment
        fields = ['name', 'email', 'content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'usercomment mt-2'
            })
        }


class BillingInfoForm(forms.ModelForm):
    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-input register-input', 'placeholder': 'نام خود را وارد کنید'}),
        error_messages={'required': 'وارد کردن نام الزامی است.'}
    )

    last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-input register-input', 'placeholder': 'نام خانوادگی'}),
        error_messages={'required': 'وارد کردن نام خانوادگی الزامی است.'}
    )

    # اصلاح نام‌ها مطابق با مدل
    province = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-input register-input', 'placeholder': 'استان'}),
        error_messages={'required': 'استان را وارد کنید.'}
    )

    street = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-input register-input', 'placeholder': 'آدرس خیابان'}),
        error_messages={'required': 'آدرس خیابان را وارد کنید.'}
    )

    postal_code = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-input register-input', 'placeholder': 'کد پستی'}),
        error_messages={'required': 'کد پستی الزامی است.'}
    )

    phone_number = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-input register-input', 'placeholder': 'شماره تلفن'}),
        error_messages={'required': 'شماره تلفن الزامی است.'}
    )

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={'class': 'form-input register-input', 'placeholder': 'ایمیل'}),
        error_messages={'required': 'وارد کردن ایمیل الزامی است.',
                        'invalid': 'فرمت ایمیل صحیح نیست.'}
    )

    class Meta:
        model = BillingInfo
        fields = [
            'first_name', 'last_name', 'province', 'street',
            'postal_code', 'phone_number', 'email'
        ]
