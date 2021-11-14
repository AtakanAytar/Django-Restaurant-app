from django.contrib import admin
from .models import *
# Register your models here.


admin.site.register(menu_item)
admin.site.register(user_info)
admin.site.register(qr_link_resolve)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Message)
admin.site.register(Room)
admin.site.register(branch_info)
admin.site.register(review)