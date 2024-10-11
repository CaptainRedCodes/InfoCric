from .views import serieslist
from django.urls import path

app_name='serieslist'

urlpatterns=[
    path('',serieslist,name='serieslist'),
]