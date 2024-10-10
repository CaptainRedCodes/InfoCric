from django.urls import path
from .views import matchlist

urlpatterns = [
    path('', matchlist, name='matchlist'),  # Search page
]

