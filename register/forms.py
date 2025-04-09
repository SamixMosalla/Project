from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-input register-input',
        'placeholder': 'ایمیل '
    }))
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={
        'class': 'form-input register-input',
        'placeholder': 'نام و نام خانوادگی'
    }))

    class Meta:
        model = User
        fields = ('first_name', 'username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-input register-input',
                'placeholder': 'نام کاربری'
            }),
            'password1': forms.PasswordInput(attrs={
                'class': 'form-input register-input',
                'placeholder': 'پسورد'
            }),
            'password2': forms.PasswordInput(attrs={
                'class': 'form-input register-input',
                'placeholder': 'تکرار پسورد'
            }),
        }
        error_messages = {
            'username': {
                'required': 'لطفاً نام کاربری را وارد کنید.',
                'unique': 'این نام کاربری قبلاً ثبت شده است.'
            },
            'email': {
                'required': 'لطفاً ایمیل خود را وارد کنید.',
                'invalid': 'ایمیل وارد شده معتبر نیست.'
            },
            'password1': {
                'too_short': 'رمز عبور خیلی کوتاه است. حداقل باید ۸ کاراکتر داشته باشد.',
                'too_common': 'این رمز عبور خیلی متداول است.',
                'only_numeric': 'رمز عبور نمی‌تواند فقط شامل اعداد باشد.',
            },
            'password2': {
                'password_mismatch': 'رمز عبور با تکرار آن مطابقت ندارد.'
            },
        }

    def clean_password1(self):
        password = self.cleaned_data.get("password1")

        if not password:
            raise ValidationError("رمز عبور نمی‌تواند خالی باشد.")

        if len(password) < 8:
            raise ValidationError(
                "رمز عبور خیلی کوتاه است. حداقل باید ۸ کاراکتر داشته باشد.")

        if password.isnumeric():
            raise ValidationError("رمز عبور نمی‌تواند فقط شامل اعداد باشد.")

        common_passwords = ["password", "12345678", "qwerty", "abcdefgh"]
        if password.lower() in common_passwords:
            raise ValidationError("این رمز عبور خیلی متداول است.")

        return password

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if not password2:
            raise ValidationError("تکرار رمز عبور نمی‌تواند خالی باشد.")

        if len(password2) < 8:
            raise ValidationError(
                "تکرار رمز عبور خیلی کوتاه است. حداقل باید ۸ کاراکتر داشته باشد.")

        if password2.isnumeric():
            raise ValidationError(
                "تکرار رمز عبور نمی‌تواند فقط شامل اعداد باشد.")

        return password2

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError("رمز عبور با تکرار آن مطابقت ندارد.")

        return cleaned_data


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-input login-input',
        'placeholder': 'ایمیل یا نام کاربری'
    }))

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input login-input',
            'placeholder': 'پسورد'
        })
    )

    error_messages = {
        "invalid_login": "نام کاربری یا رمز عبور اشتباه است. لطفاً دوباره تلاش کنید.",
        "inactive": "حساب کاربری شما غیرفعال است.",
    }

    username = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-input login-input',
        'placeholder': 'ایمیل یا نام کاربری'
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-input login-input',
        'placeholder': 'رمز عبور'
    }))

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                "حساب کاربری شما غیرفعال است.", code="inactive")
