from django.shortcuts import render

# Create your views here.
from django.urls import path
from django.conf.urls import url, include
from . import views
from django.conf import settings #add this
from django.conf.urls.static import static #add this
from hub.models import *

urlpatterns = [
    
    path('login_page', views.login_page, name='login'),
    path("private_profile",views.private_profile_checker,name="private_profile"),
    path("manage_users",views.manage_users),
] 



