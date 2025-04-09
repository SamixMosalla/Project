from django.urls import path
from main import views
from .views import main_view, product_page, ProductDetailView, add_to_cart, cart_view, BlogDetailView, remove_from_cart, update_cart, user_logout , checkout_view
urlpatterns = [
    path('', main_view, {'template_name': 'main/index.html'}, name='index'),

    path('about/', main_view,
         {'template_name': 'main/about.html'}, name='about'),

    path('contact/', views.contact_view, name='contact'),

    path('product/<int:pk>/<str:name>',
         ProductDetailView.as_view(), name='product_detail'),

    path('blog/<int:pk>/<str:name>', BlogDetailView.as_view(), name='blog_detail'),


    path("add-to-cart/", add_to_cart, name="add_to_cart"),

    path("cart/", cart_view, name="cart"),


    path("remove-from-cart/", remove_from_cart, name="remove-from-cart"),

    path("update-cart/", update_cart, name="update-cart"),

    path('logout/', user_logout, name='logout'),

    path('payment/', checkout_view, name='payment')
]
