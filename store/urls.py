from django.urls import path
from store import views
from .views import main_view , product_list

urlpatterns = [
    path('store/', product_list,
         {'template_name': 'store/store.html'}, name='store'),
]
