from django.db import models
import uuid
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=200, blank=False)
    
    def __str__(self):
        return self.title

class Products(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey(Category, related_name="category", on_delete=models.CASCADE)
    name = models.CharField(max_length=200, blank=False)
    price = models.FloatField(blank=False)
    available_quantity = models.IntegerField(blank=False, default=0)
    in_stock = models.BooleanField(default=False)
    image_url = models.URLField(max_length=500, blank=False)
    public_id = models.CharField(max_length=200, blank=True)
    
    def __str__(self):
        return self.name
    
class Our_user(models.Model):
    id = models.CharField(primary_key=True, default=uuid.uuid4, blank=False)
    user = models.OneToOneField(User,blank=False, on_delete=models.CASCADE)
    username = models.CharField(max_length=200, unique=True, blank=False)
    email = models.EmailField(blank=False, unique=True)
    password = models.CharField(blank=False)
    
    def __str__(self):
        return self.username
    
class Cart(models.Model):
    user = models.OneToOneField(Our_user, related_name="user_cart", on_delete=models.CASCADE)
    total_cost = models.FloatField(blank=False, default=0)
    
    def __str__(self):
        return self.user
    
class CartItem(models.Model):
    item = models.ForeignKey(Cart, related_name="cart_item", on_delete=models.CASCADE)
    product_id = models.CharField(blank=False, max_length=200)
    product_name = models.CharField(max_length=200, blank=False)
    quantity = models.IntegerField(blank=False, default=0)
    price = models.FloatField(blank=False)
    
    
    def __str__(self):
        return self.product_name
    
    
