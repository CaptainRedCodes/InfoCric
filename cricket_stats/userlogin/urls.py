from django.urls import path
from django.contrib.auth import views as auth_views
from .views import signup

app_name='userlogin'

urlpatterns=[
    path('login/', auth_views.LoginView.as_view(template_name='userlogin/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(next_page='userlogin:login'),name='logout'),
    path('signup/',signup,name='signup'),
    #path('profile/',Profile.as_view(),name='profile')
]