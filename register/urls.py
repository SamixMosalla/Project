from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_or_login, {'template_name': 'register/login.html'} , name='register'),
]