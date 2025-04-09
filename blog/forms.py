from django import forms
from .models import Subscriber


class SubscriberForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['email']
        labels = {
            'email': ''
        }
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'input-of-email',
                'placeholder': 'پست الکترونیکی',

            })
        }
        error_messages = {
            'email': {
                'required': 'لطفا ایمیل خود را وارد کنید ',
                'invalid': 'این ایمیل نامعتبر است',
                'unique': 'این ایمیل قبلا ثبت شده است ',
            }
        }
