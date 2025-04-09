# forms.py
from django import forms
from .models import BulkOrder

class BulkOrderForm(forms.ModelForm):
    class Meta:
        model = BulkOrder
        fields = ['first_name', 'last_name', 'phone', 'whatsapp', 'email', 'amount_kg']
