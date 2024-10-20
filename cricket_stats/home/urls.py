from django.urls import path
from .views import home_view as home

app_name='home'

urlpatterns=[
    path('',home,name='home'),
]