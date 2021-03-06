"""smartData URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path
from django.views.generic.base import TemplateView
from django.conf.urls import url

from frontEnd import views
from frontEnd import industries
from frontEnd import marketOverview
from frontEnd import dataManagerView
from frontEnd import industry
from frontEnd import stockView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('rr', views.dataManagerReserveRequirement),
    path('cpi', views.dataManagerCpi),
    #path('ppi', views.dataManagerPpi),
    #path('pmi', views.dataManagerPmi),
    path('', views.homePage),
    path('industries', industries.main),
    url(r'^industry/$', industry.main),
    url(r'^tsCode/$', stockView.main),
    path('marketOverview', marketOverview.main),
    path('dataManager', dataManagerView.main),

    #path('vue/', TemplateView.as_view(template_name="vue.html")),
]
