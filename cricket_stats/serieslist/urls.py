from .views import serieslist
from django.urls import path

urlpatterns=[
    path('',serieslist,name='serieslist'),
]