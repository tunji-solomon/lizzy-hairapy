from django.shortcuts import render, redirect
from .models import *
from cloudinary.uploader import upload
from django.contrib.auth import login,logout,authenticate
from django.core.paginator import Paginator
from django.contrib import messages
import re
import time


# Create your views here.
saved_paginated_products = None
def home(request, page=None):
    global saved_paginated_products
    global all_product
        
    categories = Category.objects.all()
    price_by = request.GET.get("price")
    category = request.GET.get("category")
    search = request.GET.get("search")
    page = request.GET.get("page")
    
    if not page:
        saved_paginated_products = Products.objects.all()
        
    
    if price_by or category  or search:
        saved_paginated_products = None

        if search is not None:
            saved_paginated_products = Products.objects.filter(name__icontains=search)
        else:
            if price_by:
                price = request.GET.get("price-field")
                if price_by == ">":
                    if price and category:
                        all_product = Products.objects.filter(price__gt = price, category__title = category)
                    if price and not category:
                        all_product = Products.objects.filter(price__gt = price)
                    if not price and category:
                        all_product = Products.objects.filter(category__title = category)
                else:
                    if price and category:
                        all_product = Products.objects.filter(price__lt = price, category__title = category)
                    if price and not category:
                        all_product = Products.objects.filter(price__lt = price)
                    if not price and category:
                        all_product = Products.objects.filter(category__title = category) 
                        
            else:
                if category:
                    all_product = Products.objects.filter(category__title = category)
            saved_paginated_products = all_product
            
            
    paginated_product = Paginator(saved_paginated_products.order_by("price"), 1)
    product_pages = paginated_product.get_page(page)
    all_product = product_pages
    context = {
        "categories" : categories,
        "products" : all_product
    }
    
     
    return render(request, 'home.html', context)

def add_product(request):
    
    if request.method == "POST":
        category_name = request.POST.get('category').strip().capitalize()
        category = Category.objects.get(title=category_name)
        name = request.POST.get("name").strip().capitalize()
        price = float(request.POST.get("price"))
        quantity = int(request.POST.get("quantity"))
        image = request.FILES.get("image")
        result = upload(image)
        image_url = result.get("secure_url")
        public_id = result.get("public_id")
        new_product = Products.objects.create(name=name, category=category, price=price, 
                    available_quantity=quantity, in_stock = True if quantity > 0 else False,
                    image_url=image_url, public_id=public_id
                    )
        
        new_product.full_clean()
        new_product.save()
        
        return redirect("home")
    categories = Category.objects.all()
    return render(request, "add_product.html", {"categories":categories})

def register(request):
    password_pattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[\dA-Za-z]).{8,15}$'
    if request.method == "POST":
        username:str = request.POST.get("username")
        email:str = request.POST.get("email")
        password:str = request.POST.get("password")
        confirm:str = request.POST.get("confirm")
        context = {
            "username" : username,
            "email" : email,
            "password" : password,
            "confirm" : confirm
        }
        
        if Our_user.objects.filter(username=username).exists() == False:
            if Our_user.objects.filter(email=email).exists() == False:
                print("PASSWORD:",password)
                if password == confirm:
                    if re.match(password_pattern, password.strip()):
                        
                        user = User.objects.create(username=username,email=email,password=password)
                        user.save()
                        new_user = Our_user(user=user,username=username,email=email,password=password)
                        new_user.clean_fields()
                        new_user.save()
                        messages.success(request, "User registraion successful", extra_tags= "success")
                        return redirect("home")
                    else:
                        messages.info(request, "Password does not match the required pattern", extra_tags= "pattern")
                        return render(request, "registration.html", {"context": context})
                else:
                    print("confirm password does not match")
                    print(context)
                    messages.info(request, "Password and confirm password mismatch", extra_tags= "mismatch")
                    return render(request, "registration.html", {"context":context})
            else:
                print("Email not valid")
                messages.info(request, "User with email already exist", extra_tags= "email")
                return render(request, "registration.html", {"context": context})
        else:
            print("user with name already exist")
            messages.info(request, "User with username already exist", extra_tags= "username")
            return render(request, "registration.html", context)
    else:
        return render(request, "registration.html")
    

def login(request):
        if request.method == 'POST':
           username= request.POST.get('username')
           password = request.POST.get('password')
           user = authenticate(username=username,password=password)
           if user is not None:
               login(request,user)
               return redirect('home')
           else:
               messages.error(request, "Ivalid credentials", extra_tags="wrong_credentials")
        return render(request,'login.html')
    
                
        
    

    
            
        
        
        
        
    
    
    
