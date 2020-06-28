"""Reddinfo URL Configuration

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
from reddata.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user_search/', user_search_view, name="User_search"),
    path('options/', options_view, name='Options'),
    path('post_data/', posts_view, name="Posts"),
    path('comments_data/', comments_view, name="Comments"),
    path('user_data/', profile_view, name='Profile')
]
