"""
URL configuration for ZHIN project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, re_path
from django.contrib.staticfiles.views import serve
from django.views.generic.base import RedirectView
from .api import api

urlpatterns = [
    path("admin/", admin.site.urls),
    # 配置生产环境静态文件服务，先收集静态文件，然后配置路由
    re_path(r'static/(?P<path>.*)$', lambda request, path, insecure=True, **kwargs: serve(request, path, insecure, **kwargs), name='static'),
    # 配置favicon.ico的重定向，同时需要配置 STATICFILES_DIRS 
    re_path(r'^favicon\.ico$', RedirectView.as_view(url=r'static/ilovebasketball.svg')),
    
    path("api/", api.urls),
]
