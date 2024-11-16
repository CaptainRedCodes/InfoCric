# your_app/urls.py
from django.urls import path
from .views import PlayerSearchView

app_name='stats'
urlpatterns = [
    path('', PlayerSearchView.as_view()   , name='search_cricketer'),  # Search page
]
