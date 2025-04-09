from django.urls import path
from store import views
from .views import main_view, store_view

urlpatterns = [
    path('store/', store_view,
         {'template_name': 'store/store.html'}, name='store'),
    path('filter-products/', views.filter_products, name='filter_products'),
]
