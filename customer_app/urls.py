from django.urls import path
from django.conf.urls import url, include
from . import views
from django.conf import settings #add this
from django.conf.urls.static import static #add this


urlpatterns = [
    
    path("resolve_url/<str:string_info>",views.resolve_qr_code),
    path("sepet",views.cart_page),
    path("review",views.customer_review),
  
] 