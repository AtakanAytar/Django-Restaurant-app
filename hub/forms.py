from django import forms
from .models import *
  
class HotelForm(forms.ModelForm):
  
    class Meta:
        model = menu_item
        fields = ['title', 'food_item_name',"details","price","restaurant_id","branch_id","menu_pic"]

