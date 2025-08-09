from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register([Products, Category, Our_user, Cart, CartItem, Pending_Order, Pending_order_items])
