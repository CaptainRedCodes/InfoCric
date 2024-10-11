# your_app/urls.py
from django.urls import path
from .views import search_cricketer

app_name='stats'
urlpatterns = [
    path('', search_cricketer, name='search_cricketer'),  # Search page
]
