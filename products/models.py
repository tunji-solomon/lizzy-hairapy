from django.db import models
import uuid

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
