from django.urls import path
from .views import main_view, send_newsletter

urlpatterns = [
    path('blog/', main_view,
         {'template_name': 'blog/weblog-main.html'}, name='blog'),
    path('blogs/', send_newsletter, name='send_newsletter'),
]
