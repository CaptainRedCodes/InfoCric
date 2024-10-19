from django.urls import path
from .views import filter_stats

app_name='filter_stats'
urlpatterns=[
    path('stats/',filter_stats,name='filter_stats')
]