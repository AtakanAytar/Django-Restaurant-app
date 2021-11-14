from django.db import models
from django.contrib.auth.models import User
from datetime import date, datetime
from django.db.models.deletion import PROTECT
from django.utils.crypto import get_random_string
from django.conf import settings
from django.shortcuts import reverse



class qr_link_resolve(models.Model):
    qr_code_id = models.CharField(max_length=50 ) 
    restaurant_id = models.CharField(max_length=500)
    branch_id = models.CharField(max_length=500)
    table_id = models.IntegerField(default=-1)

   
#######
class menu_item(models.Model):
    title = models.CharField(max_length=200)
    food_item_name = models.CharField(max_length=200)
    details = models.CharField(max_length=200)
    price = models.CharField(max_length=200)
    restaurant_id = models.CharField(max_length=500)
    branch_id = models.CharField(max_length=500)
    menu_pic = models.ImageField(null=True)

    class Meta:
        ordering = ['title'] 
    
    def __str__(self):
        return self.food_item_name

    def get_absolute_url(self):
        return reverse("core:product", kwargs={
            "pk" : self.pk
        
        })

    def get_add_to_cart_url(self) :
        return reverse("core:add-to-cart", kwargs={
            "pk" : self.pk
        })

    def get_remove_from_cart_url(self) :
        return reverse("core:remove-from-cart", kwargs={
            "pk" : self.pk
        }) 

class OrderItem(models.Model) :
    session_id = models.CharField(max_length=50 , default="none")
    ordered = models.BooleanField(default=False)
    
    item = models.ForeignKey(menu_item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    
    
    

    def __str__(self):
        return f"{self.quantity} of {self.item.food_item_name}"

    def get_total_item_price(self):
        price = int(self.quantity) * int(self.item.price)
        print(price)
        return price


class Order(models.Model) :
    session_id = models.CharField(max_length=50 , default="none")
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    restaurant_id = models.CharField(max_length=500)
    branch_id = models.CharField(max_length=500)
    
    table_id = models.IntegerField(default=-1)
    def _str_(self):
        return self.user.username
    def get_total_price(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_total_item_price()
        return total

class user_info(models.Model):
    username = models.CharField(max_length=200)
    status_id = models.IntegerField(default=-1)    #garson 0 - müdür 1 - yönetici 2
    restaurant_id = models.CharField(max_length=500)
    branch_id = models.CharField(max_length=500) # -1 means all acssess

class Room(models.Model):
    name = models.CharField(max_length=1000)
    restaurant_id = models.CharField(max_length=500)
    branch_id = models.CharField(max_length=500)
    room_clearance = models.IntegerField(default=0)
    
class Message(models.Model):
    value = models.CharField(max_length=1000000)
    date = models.DateTimeField(default=datetime.now, blank=True)
    sender = models.CharField(max_length=1000000)
    done = models.BooleanField(default=False)
    room = models.CharField(max_length=1000000)
    restaurant_id = models.CharField(max_length=500)
    branch_id = models.CharField(max_length=500)
    table_id = models.IntegerField(default=-1)
    
class branch_info(models.Model):
    restaurant_id = models.CharField(max_length=500)
    branch_id = models.CharField(max_length=500)
    latitude = models.FloatField(max_length=100)
    longtitute = models.FloatField(max_length=100)
    
    
class review(models.Model):
    value = models.CharField(max_length=1000000)
    stars = models.IntegerField()

    

