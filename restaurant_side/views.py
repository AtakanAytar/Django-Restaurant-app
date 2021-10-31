from django.shortcuts import render , redirect , get_object_or_404
from django.http import HttpResponse, request
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.models import Group , Permission
import re
from django.contrib.auth import logout
from hub.models import *
from django.http import HttpResponse, JsonResponse
from django.utils import timezone


def get_user_permissions(request):
        user_instance = user_info.objects.get(username = request.user.username)
        branch_id =  user_instance.branch_id
        restaurant_id = user_instance.restaurant_id
        status_id = user_instance.status_id
        return branch_id , restaurant_id , status_id , user_instance




def login_page(request):
        if request.method == 'POST':
                username = request.POST['username']
                password = request.POST['password']

                user = auth.authenticate(username = username, password =password  )

                if user is not None:
                        auth.login(request , user)
                        return redirect('/')    
                else:
                        messages.info(request, 'invalid username or password')
                        return redirect("/")

    
        return render(request,'login_page.html')



def private_profile_checker(request):
        branch_id , restaurant_id , status_id ,user_instance= get_user_permissions(request)
        if request.user.is_authenticated and (status_id ==1 or status_id == 2):
                return render(request,"private_profile.html")
        else:
                return redirect("/")

def add_user_from_branch(username,password,status_to_be_set,restaurant_id,branch_id):
      
        user = User.objects.create_user(username = username , password = password , email = "example@e.com" ,is_active = True )
        user_info.objects.create(username=username , status_id =status_to_be_set,restaurant_id=restaurant_id ,branch_id = branch_id)
        
        
        return None
def delete_user_from_branch(request,username):
        branch_id , restaurant_id , status_id ,user_instance= get_user_permissions(request)
        if user_instance.username != username:
                
                
                u = User.objects.get(username = username)
                perms = user_info.objects.get(username=username)

                if perms.restaurant_id == restaurant_id and (status_id  > perms.status_id or status_id == 2):
                        
                        u.delete()
                        perms.delete()
        return redirect("/manage_users")



def manage_users(request):
        branch_id , restaurant_id , status_id ,user_instance= get_user_permissions(request)
        if request.method == 'POST':
                
                if status_id ==1 or status_id == 2 and "add_user" in request.POST:
                        username = request.POST['username']
                        password= request.POST['password']
                        password2= request.POST['password2']
                        status_id_to_set = request.POST["status"]
                        branch_id_to_set = request.POST["branch_id"]
                        print("yep")
                        if status_id == 1:
                                branch_id_to_set = branch_id
                        
                        if status_id >= int(status_id_to_set) >= 0:

                                if password == password2 and len(password) > 7:
                                        print("yep2")
                                        add_user_from_branch(username,password,status_id_to_set,restaurant_id,branch_id_to_set)
                elif "delete_user" in request.POST:
                    user_to_be_deleted = request.POST["username"]
                    delete_user_from_branch(request,user_to_be_deleted)
                    

                
                else:
                        return redirect("/")

        users_all=""
        if status_id == 1 :
                users_all = user_info.objects.filter(restaurant_id=restaurant_id , branch_id=branch_id)
        elif status_id==2:
                users_all = user_info.objects.filter(restaurant_id=restaurant_id , branch_id=branch_id)

        context = { 'query_results' : users_all }
        return render(request,"manage_users.html" , context)
