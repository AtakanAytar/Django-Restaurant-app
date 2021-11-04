from django.urls import path
from django.conf.urls import url, include
from . import views
from django.conf import settings #add this
from django.conf.urls.static import static #add this


urlpatterns = [
    
    path('', views.landing_page, name='landing_page'),
 
    path('signup_page', views.signup_page, name='signup' ),
    path("logout",views.log_user_out,name="logout"),
    path("private_profile",views.private_profile,name="private_profile"),
    
    
   
    

    
    
   
  
  

    



    path("get_messages_page/<str:room_name>",views.get_messages_page)
] 

urlpatterns += static(settings.MEDIA_URL,document_root =settings.MEDIA_ROOT)