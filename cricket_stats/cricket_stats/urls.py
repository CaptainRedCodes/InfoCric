"""
URL configuration for cricket_stats project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('stats/',include('stats.urls')),
    path('matches/',include('matchlist.urls')),
    path('serieslist/',include('serieslist.urls')),
    path('',include('home.urls')),
    path('accounts/',include('userlogin.urls')),
    path('oauth/', include('social_django.urls', namespace='social')),
    path('filter/',include('filterstats.urls')),
    path('ipl/v1/',include('ipl_analysis.urls')),

    #path('auction/',include('auction.urls')),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
handler404='cricket_stats.views.custom_404'