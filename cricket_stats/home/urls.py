from django.urls import path
from .views import home_view as home,news_page

app_name='home'

urlpatterns=[
    path('',home,name='home'),
    path('news/<str:article_id>/<slug:headline>', news_page, name='news_page')

]
