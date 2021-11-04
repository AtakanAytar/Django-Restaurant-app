from django.shortcuts import render , redirect , get_object_or_404
from django.http import HttpResponse, request
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.models import Group , Permission
import re
from django.contrib.auth import logout
from .models import *
from .forms import *
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
# Create your views here.

## branch_id restaurant_id -1 e dikkat et
def send(request , message , sender , room , restaurant_id ,branch_id,table_id):
    

    new_message = Message.objects.create(value=message, sender=sender, room=room , restaurant_id=restaurant_id , branch_id=branch_id , table_id=table_id)
    new_message.save()
    return HttpResponse('Message sent successfully')

def landing_page(request):
        
    
        return render(request,'landing_page.html')


#def setsession(request):  
#    request.session['name'] = 'prady'  
#    return HttpResponse("session is set")  
#def getsession(request):  
#    fname = request.session['name']  
    
#    return HttpResponse(fname);  








def  signup_page(request):
        
   
    if request.method == 'POST':
        

        email = request.POST['email']
        username = request.POST['username']
        password= request.POST['password']
        password2= request.POST['password2']
        if password == password2:
                if len(password) > 7:
                        capital_letter = bool(re.match(r'\w*[A-Z]\w*', password))
                        lower_letter = bool(re.match(r'\w*[a-z]\w*', password))
                        number = bool(re.match(r'\w*[0-9]\w*', password))
                        if capital_letter and lower_letter and number:  
                                user = User.objects.create_user(username = username , password = password , email = email ,is_active = True )
                               
                                

                                user.save()
                                user_info.objects.create(username=username)
                              
                                messages.info(request, 'user created!')
                                return redirect('/login_page')
                        else: 
                                messages.info(request, 'password should contain upper and lower characters also numbers')
                                return redirect('/signup_page')
                        
                else:
                        messages.info(request, 'passwords should be longer than 7')
                        return redirect('/signup_page')
               
        else:
                messages.info(request, 'passwords dont match!')
                return redirect('/signup_page')
                
                
        


   

        

    return render(request,"signup_page.html")


def log_user_out(request):
        if request.user.is_authenticated:
                logout(request)
                request.session.flush()
        return redirect("/")



def get_user_permissions(request):
        user_instance = user_info.objects.get(username = request.user.username)
        branch_id =  user_instance.branch_id
        restaurant_id = user_instance.restaurant_id
        status_id = user_instance.status_id
        return branch_id , restaurant_id , status_id , user_instance










def private_profile(request):
        branch_id , restaurant_id , status_id ,user_instance= get_user_permissions(request)
        if request.user.is_authenticated and (status_id ==1 or status_id == 2):
                return render(request,"private_profile.html")
        else:
                return redirect("/")














def  get_messages_page(request,room_name):
        branch_id , restaurant_id , status_id ,user_instance= get_user_permissions(request)
        messages = Message.objects.filter(room=room_name,  restaurant_id=restaurant_id,branch_id=branch_id , done = False )
        context = { 'query_results' : messages}


        if request.method =="POST":
             
                if "done_message" in request.POST:
                        print("hey")
                       
                        message = request.POST["delete_item"]
                        
                        messages = Message.objects.get(value = message ,room=room_name,  restaurant_id=restaurant_id,branch_id=branch_id , done = False )
                        messages.done = True 
                        messages.save()
                        if room_name =="siparişler":
                                send(request=request,message = message[1] + "siparişi hazır" , sender="Mutfak" ,room="masalar" , restaurant_id=restaurant_id , branch_id=branch_id , table_id="-99" )


                        messages = Message.objects.filter(room=room_name,  restaurant_id=restaurant_id,branch_id=branch_id , done = False )
                        context = { 'query_results' : messages}
                        
                        
                        return render(request,"get_messages.html" , context )
                        

        return render(request,"get_messages.html" , context )













