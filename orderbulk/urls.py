from django.urls import path
from .views import *

urlpatterns = [
    path('orderbulk/', bulk_order_view, name='orderbulk')
]
