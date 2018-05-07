"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from myblog import views
#from myblog import urls as mysite_urls

urlpatterns = [
    #add the website you want to show
    #path('admin/', admin.site.urls),
    path(r'index/',views.index,name='index'),
    path(r'register/',views.register,name='register'),
    path(r'login/',views.log_in,name='login'),
    path(r'logout/',views.log_out,name='logout'),
    path(r'^(?P<article_id>[0-9]+)/comment/$',views.comment,name='comment'),
    path(r'^(?P<article_id>[0-9]+)/keep/$',views.get_keep,name='keep'),
    path(r'^(?P<article_id>[0-9]+)/poll/$',views.get_poll_article,name='poll'),
    path(r'^(?P<article_id>[0-9]+)/$',views.article,name='article'),
    path(r'admin/', admin.site.urls),
]
