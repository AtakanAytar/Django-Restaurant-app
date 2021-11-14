from django.db.models.lookups import StartsWith
from django.shortcuts import render , redirect , get_object_or_404
from django.http import HttpResponse, request
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.models import Group , Permission
import re
from django.contrib.auth import logout
from .models import *
from hub.models import *
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from geopy.distance import geodesic 
# Create your views here.


def send(request , message , sender , room , restaurant_id ,branch_id,table_id):
    
    if not Message.objects.filter(value=message, sender=sender, room=room , restaurant_id=restaurant_id , branch_id=branch_id , table_id=table_id , done = False).exists():

        new_message = Message.objects.create(value=message, sender=sender, room=room , restaurant_id=restaurant_id , branch_id=branch_id , table_id=table_id)
        new_message.save()
        return HttpResponse('Message sent successfully')



def public_profile(request , restaurant_id , branch_id , table_no ):
        session_key  = request.session.session_key
        menu_of_requested = menu_item.objects.filter(restaurant_id=restaurant_id , branch_id=branch_id)
        menu_titles = menu_of_requested.values_list("title",flat=True)
        menu_titles = list(dict.fromkeys(menu_titles))
        context = { 'query_results' : menu_of_requested ,"menu_titles":menu_titles } 
        request.session['public_profile'] =  request.get_full_path()

        if request.method == 'POST':
                if "add_item" in request.POST:
                        
                        food_item_name = request.POST["add_item"]
                        pk = food_item_name
                       
                        item = get_object_or_404(menu_item, food_item_name = food_item_name )
                        order_item, created = OrderItem.objects.get_or_create(
                        item=item,
                        session_id = session_key,
                        ordered = False
                        )
                        order_qs = Order.objects.filter(session_id=session_key, ordered= False)
                        
                        
                        
                        if order_qs.exists() :
                                order = order_qs[0]
                                if order.items.filter(item__pk = item.pk).exists() :
                                        order_item.quantity += 1
                                        order_item.save()
                                        messages.info(request, "Added quantity Item")
                                else:
                                        order.items.add(order_item)
                                        messages.info(request, "Item added to your cart")
                       
                        
                        else:
                                ordered_date = timezone.now()
                                order = Order.objects.create(session_id=session_key, ordered_date = ordered_date , restaurant_id=restaurant_id,branch_id=branch_id,table_id=table_no)
                                order.items.add(order_item)
                                messages.info(request, "Item added to your cart")
                        
                elif "garson_çağır" in request.POST:
                        print("here")
                        message = str(table_no) + " garson çağırıyor"
                        
                        send(request,message,table_no,"masalar",restaurant_id,branch_id,table_no)
                elif "hesap_istemek" in request.POST:
                        total_price = 0

                        message = str(table_no) + " hesap istiyor"
                        order_qs = Order.objects.filter(session_id=session_key, ordered= True,paid=False)
                        for a in order_qs:
                                for b in a.items.all():
                                        curr_price = int(b.item.price) * int(b.quantity)
                                        item_row = str(b.quantity) +"  " + str(b.item) + "  " + str(b.item.price) + " " + str(curr_price)
                                        message = message + " " + item_row
                                        total_price = total_price + curr_price 
                        message = message + "total: " + str(total_price)
                        #Burada olcak hesap
                       
                        send(request,message,table_no,"masalar",restaurant_id,branch_id,table_no)

        return render(request,"new_public_profile.html" , context)

def resolve_qr_code(request , string_info):
        request.session.set_expiry(600)
        if  len(string_info) < 40:
                string_info = str(string_info).split("-")
                
                user_coord = (float(string_info[0]),float(string_info[1]))


                branch_result = branch_info.objects.get(restaurant_id = request.session['restaurant_id'] , branch_id =  request.session['branch_id'] )
               
                
                branch_coord = (branch_result.latitude,branch_result.longtitute)
                if geodesic(user_coord, branch_coord).km < 0.15 or branch_result.latitude == -1 :
                        print(geodesic(user_coord, branch_coord).km)
                        return  public_profile(request,request.session['restaurant_id'],request.session['branch_id'],request.session['table_id']  )
        else:
        
                qr_object_result = qr_link_resolve.objects.get(qr_code_id = string_info)
                restaurant_id = qr_object_result.restaurant_id
                branch_id =  qr_object_result.branch_id
                table_id =  qr_object_result.table_id
        
       
                request.session['restaurant_id'] = restaurant_id
                request.session['branch_id'] = branch_id
                request.session['table_id'] = table_id
                
      
        
        return render(request,"geolocation.html")



        
        













def cart_page(request):
      
        session_key  = request.session.session_key
        order = Order.objects.filter(session_id=session_key, ordered=False)
        if not order.exists():
                return redirect(request.session['public_profile'])

        order = order[0]
        print(order)
        restaurant_id = order.restaurant_id
        branch_id = order.branch_id
        table_id = order.table_id
        context = {"object":order}
        
        if request.method == "POST":
                print("e")
                if "delete_item" in request.POST:
                        food_item_name = request.POST["delete_item"]
               
                        
                        item = get_object_or_404(menu_item, food_item_name=food_item_name )
                        order_qs = Order.objects.filter(
                        session_id=session_key, 
                        ordered=False
                        )
                        if order_qs.exists():
                                order = order_qs[0]
                                if order.items.filter(item__pk=item.pk).exists():
                                        order_item = OrderItem.objects.filter(
                                        item=item,
                                        session_id=session_key,
                                        ordered=False
                                )[0]
                        order_item.delete()
                elif "make_the_order" in request.POST:
                        order_string =  str(table_id) + " "
                        items = order.items.all()
                        for a in items:
                                
                                order_message =  a.item.food_item_name + " x " + str(a.quantity) + " "
                                order_string = order_string + order_message
                        order.ordered = True
                        order.save()
                        send(request,order_string,session_key,"siparişler",restaurant_id,branch_id,table_id)
                        return redirect(request.session['public_profile'])
                elif "menuye_don" in request.POST:
                        print("saw")
                        return redirect(request.session['public_profile'])


                                



        return render(request,"cart_page.html",context)

def customer_review(request):
        if request.method == "POST":
                
                if "message" in request.POST:
                        Message = request.POST["message"]
                        Stars = request.POST["stars"]
                        new_message = review.objects.create(value=Message, stars=Stars)
                        new_message.save()
                        


        return render(request,"post_review.html")