from django.urls import path
from .views import coming_soon

app_name='auction'

urlpatterns=[
    path('soon/',coming_soon,name='coming_soon'),
]