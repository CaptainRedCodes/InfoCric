from django.urls import path
from .views import matchlist

app_name='matchlist'
urlpatterns = [
    path('', matchlist, name='matchlist'),  # Search page
]

