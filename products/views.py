from django.shortcuts import render, redirect
from .models import *
from cloudinary.uploader import upload, destroy
from django.contrib.auth import login,logout,authenticate
from django.core.paginator import Paginator
from django.contrib import messages
import re
import random
from django.db.models import Q
from .tasks import send_welcome_email
import datetime


# Create your views here.
saved_paginated_products = None
def home(request, page=None):
    if request.user.is_superuser == False:
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
                
        if request.user.is_authenticated:
            if request.user.is_authenticated:
                user = Our_user.objects.get(username = request.user.username)
                
                cart_exist = Cart.objects.filter(user=user).first() 
                try:
                    global cart_count
                    cart_count = len(cart_exist.cart_item.all()) 
                except Exception:
                    cart_count = None
        else:
            cart_count = None
                
        paginated_product = Paginator(saved_paginated_products.order_by("price"), 20)
        product_pages = paginated_product.get_page(page)
        all_product = product_pages
        context = {
            "categories" : categories,
            "products" : all_product,
            "cart_count" : cart_count
        }
        
        
        return render(request, 'home.html', context)
    
    return render(request, "admin/home.html")

def add_product(request):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method == "POST":
            category_name = request.POST.get('category').strip().capitalize()
            category = Category.objects.get(title=category_name)
            name = request.POST.get("name").strip().capitalize()
            price = float(request.POST.get("price"))
            quantity = int(request.POST.get("quantity"))
            image = request.FILES.get("image")
            try:
                result = upload(image)
            except Exception as e:
                messages.info(request, "Something went wrong, Please try again later.", extra_tags="server")
                return redirect("add-product")
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

def sign_up(request):
    password_pattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[\dA-Za-z]).{8,15}$'
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
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
            if re.match(email_pattern, email):
                if Our_user.objects.filter(email=email).exists() == False:
                    if password == confirm:
                        if re.match(password_pattern, password.strip()):
                            
                            user = User.objects.create_user(username=username,email=email,password=password)
                            user.save()
                            new_user = Our_user(user=user,username=username,email=email,password=password)
                            new_user.clean_fields()
                            new_user.save()
                            user = authenticate(request, username=username, password=password)
                            login(request, user)
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
                    messages.info(request, "User with email already exist", extra_tags= "email")
                    return render(request, "registration.html", {"context": context})
            else:
                messages.info(request, "Email not a valid email", extra_tags="valid-email")
                return render(request, "registration.html", {"context": context})
        else:
            print("user with name already exist")
            messages.info(request, "User with username already exist", extra_tags= "username")
            return render(request, "registration.html", {"context": context})
    else:
        return render(request, "registration.html")
    

def login_user(request):
        if request.method == 'POST':
           username= request.POST.get('username')
           password = request.POST.get('password')
           user = authenticate(username=username,password=password)
           if user is not None:
               login(request,user)
               subject= "LOGIN SUCCESSFUL"
               message= f"{user.username}, your account was accessed today at {datetime.date.today()}"
               recipient= [user.email,]
               try:
                    send_welcome_email.delay(subject, message, recipient)
               except Exception as e:
                       
                import traceback
                print("EMAIL ERROR:", traceback.format_exc())              

               return redirect('home')
           else:
               messages.error(request, "Invalid credentials", extra_tags="wrong_credentials")
        return render(request,'login.html')
    
    
def logout_user(request):
    logout(request)
    return redirect("home")

product_update = None
def update_product(request):
    if request.user.is_authenticated and request.user.is_superuser:
        global product_update
        products = Products.objects.all()

        if request.method == "GET":
            search = request.GET.get("search")
            if search:
                product_update = Products.objects.filter(name=search.strip()).first()

                if product_update:
                    category = Category.objects.all()
                    context = {
                        "product": product_update,
                        "categories": category,
                        "products": products
                        
                    }
                    return render(request, "admin/update.html", context)
                else:
                    product_update = None
                    messages.info(request, "Product with name does not exist", extra_tags="product")
                    return render(request, "admin/update.html", {"products": products})
            else:   
                return render(request, "admin/update.html",{"products": products })
            
        else:
            get_name = request.POST.get("name")
            get_quantity = int(request.POST.get("quantity"))
            get_price = float(request.POST.get("price"))
            get_category = request.POST.get("category")
            get_image = request.FILES.get("image")
            get_category = Category.objects.get(title=get_category)
            
            
            
            if get_image:
                try:
                    destroy(product_update.public_id)
                except Exception as e:
                    messages.info(request, "Something went wrong, please try again later", extra_tags="server")
                    return redirect("update-product")
                result = upload(get_image)
                product_update.image_url = result.get("secure_url")
                product_update.public_id = result.get("public_id")
            
                
            product_update.name = get_name
            product_update.available_quantity += get_quantity
            product_update.price = round(get_price,2)
            product_update.category = get_category
            
            product_update.save()
            
            return render(request, "admin/product_success.html")
    
    else:
        messages.info(request, "User not authorised to carry out this action", extra_tags="authorization")
        return redirect("home")
    
        
    
def create_admin(request):
    password_pattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[\dA-Za-z]).{8,15}$'
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
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
        if request.user.is_authenticated and  request.user.is_superuser:
            if Our_user.objects.filter(username=username).exists() == False:
                if re.match(email_pattern, email):
                    if Our_user.objects.filter(email=email).exists() == False:
                        if password == confirm:
                            if re.match(password_pattern, password.strip()):
                                
                                user = User.objects.create_superuser(username=username,email=email,password=password)
                                user.save()
                                new_user = Our_user(user=user,username=username,email=email,password=password)
                                new_user.clean_fields()
                                new_user.save()
                                return render(request, "reg_success.html")
                            else:
                                messages.info(request, "Password does not match the required pattern", extra_tags= "pattern")
                                return render(request, "admin/registration.html", {"context": context})
                        else:
                            messages.info(request, "Password and confirm password mismatch", extra_tags= "mismatch")
                            return render(request, "admin/registration.html", {"context":context})
                    else:
                        messages.info(request, "User with email already exist", extra_tags= "email")
                        return render(request, "admin/registration.html", {"context": context})
                else:
                    messages.info(request, "Email not a valid email", extra_tags="valid-email")
                    return render(request, "admin/registration.html", {"context": context})
            else:
                print("user with name already exist")
                messages.info(request, "User with username already exist", extra_tags= "username")
                return render(request, "admin/registration.html", {"context": context})

        else:
            messages.info(request, "User not authorised to carry out this action", extra_tags="authorization")
            return render(request, "admin/registration.html", {"context": context})
    else:
        return render(request, "admin/registration.html")
    
    
def add_to_cart(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        product_name = request.POST.get("product_name")
        product_quantity = int(request.POST.get("product_quantity"))
        product_price =float(request.POST.get("product_price"))
        product_image = request.POST.get("product_image")
        product_total = round(product_price * product_quantity, 2)

        if product_quantity > 0:
        
            if request.user.is_authenticated:
                user = Our_user.objects.get(username = request.user.username)
                
                cart_exist = Cart.objects.filter(user=user).first()
                if cart_exist:
                    for item in cart_exist.cart_item.all():
                        if item.product_id == product_id:
                            item.quantity += product_quantity
                            item.total = product_total
                            item.save()
                            break
                    else:
                        new_item = CartItem.objects.create(item=cart_exist, product_id=product_id,
                                                           product_name=product_name, quantity=product_quantity,
                                                           price=product_price,total=product_total, item_image=product_image)
                        new_item.save()
                        
                    cart_exist.total_cost += product_quantity * product_price
                    cart_exist.save()
            
                    return redirect("home")
        
                else:
                    total_cost = product_price * product_quantity
                    new_cart = Cart.objects.create(user=user)
                    new_cart.total_cost += total_cost
                    new_cart.save()
                    new_item = CartItem.objects.create(item=new_cart, product_id=product_id, product_name=product_name,
                                                       quantity=product_quantity, price=product_price,total=product_total,
                                                       item_image=product_image)
                    new_item.save()
                    return redirect("home")
                     
            return redirect("sign-up")
        
        return redirect("home")
    
    return redirect("home")
    
def view_cart(request, total_cost=None):
    
    if request.user.is_authenticated:
        global user_cart
        global existing_cart
        global item_name
        global related_product
        related_product = Products.objects.all()
        user = Our_user.objects.filter(user=request.user).first()
        try:
            user_cart = Cart.objects.get(user=user)
            existing_cart = user_cart.cart_item.all()
            if len(existing_cart) < 1:
                messages.info(request, "Cart is empty. Check out our products to add some.", extra_tags="empty-cart")
                return render(request, "cart.html", {"related_products": related_product})
            item_name = [item.product_name for item in existing_cart ]
        except Exception as e:
            messages.info(request, "User Have not added any item to cart", extra_tags="empty-cart")
            return render (request, "cart.html", {"related_products": related_product})
        products = Products.objects.all()
        if item_name:
            related_product = [product for product in products if not product.name in item_name ]
        else:
            related_product = [product for product in products] 
        # cart =  user_cart.cart_item.all()
        context = {
            "cart":existing_cart,
            "cart_total": total_cost if total_cost is not None else user_cart.total_cost,
            "cart_count": len(existing_cart),
            "related_products": related_product
        }            
        return render(request, "cart.html", context)
    else:
        return redirect("home")
    
def remove_item(request, id):
    user = Our_user.objects.get(user=request.user)
    existing_cart = Cart.objects.get(user=user)
    try:
        global getItem
        getItem = CartItem.objects.get(id=id)
        existing_cart.total_cost -= float(getItem.total)
        getItem.delete()
        existing_cart.save()
        return view_cart(request, existing_cart.total_cost)
    except Exception:
        return view_cart(request)
    
def delete_cart(request):
    user = Our_user.objects.get(user=request.user)
    cart = Cart.objects.get(user=user)
    cart.delete()
    return view_cart(request)
    
def checkout(request, context=None):
    if request.method == "POST":
        total_items_count = int(request.POST.get("total_item_count"))
        for i in range(total_items_count):
            item_name = request.POST.get(f"item-{i}-name")
            item_price = float(request.POST.get(f"item-{i}-price"))
            item_quantity = int(request.POST.get(f"item-{i}-quantity"))
            item_cost = item_price * item_quantity
            
            user = Our_user.objects.get(user=request.user)
            existing_cart = Cart.objects.get(user=user)
            existing_cart_items = CartItem.objects.filter(item=existing_cart, product_name=item_name).first()
            existing_cart_items.price = item_price
            existing_cart_items.quantity = item_quantity
            existing_cart_items.total = item_cost
            existing_cart_items.save()
            
        cart_total_cost = request.POST.get("total-cost")
        existing_cart.total_cost = cart_total_cost
        existing_cart.save()
        related_product = Products.objects.all()

        context = {
            "amount_to_pay": cart_total_cost,
            "cart_count": total_items_count,
            "related_products": related_product
            
        }
    
    return render(request, "checkout.html", context)

def payment(request):
    if request.method == "POST":
        user = Our_user.objects.get(user=request.user)
        cart = Cart.objects.get(user=user)
        payment_proof = request.FILES.get("image")
        if payment_proof:
            try:
                global result
                result = upload(payment_proof)
            except Exception as e:
                messages.info(request, "Something went wrong, Please try again later")
                amount_to_pay = cart.total_cost
                cart_count = len(cart.cart_item.all())
                related_product = Products.objects.all()
                context = {
                    "amount_to_pay": amount_to_pay,
                    "cart_count": cart_count,
                    "related_products": related_product
                }
                request.method = "GET"
                return checkout(request, context)
            
            payment_proof_image = result.get("secure_url")
            payment_prrof_public_id = result.get("public_id")

                
            global user_pending_order
            user_pending_order = Pending_Order.objects.create(user=user, total_cost=cart.total_cost, 
                                proof_of_payment=payment_proof_image, public_id=payment_prrof_public_id)
            user_pending_order.save()
            cart_items = cart.cart_item.all()
            
            for items in cart_items:
                pending_item = Pending_order_items.objects.create(order=user_pending_order, item_name=items.product_name,
                                                            item_quantity=items.quantity, item_price=items.price,
                                                            item_total_cost=items.total)
                pending_item.save()
                
            cart.delete()    
            return redirect("home")
        
    return redirect("view-cart")

def pending_orders(request):
    if request.user.is_authenticated and request.user.is_superuser:
        pending = Pending_Order.objects.all()
        if request.method == "POST":
            search_by = request.POST.get("search-by")
            query = request.POST.get("query", '')
            date = request.POST.get("date", "")
            print(search_by, query,date)
            if date:
                pending = Pending_Order.objects.filter(created_at=date).order_by("created_at")
                if not pending:
                    messages.info(request, "No order found for this date", extra_tags="date")
                    return render(request, "admin/pending_orders.html")
            else:
                if not query == "":
                    if search_by == "username":
                        try:
                            user = Our_user.objects.get(username=query)
                            pending = Pending_Order.objects.filter(user=user).order_by("created_at")
                        except Exception:
                            messages.info(request, "No order found for specified user", extra_tags="username")
                            return render(request, "admin/pending_orders.html")

                    if search_by == "orderId":
                        pending = Pending_Order.objects.filter(orderId=query).order_by("created_at")
                else:
                    return redirect("home")
                    
            # query = request.POST.get("query")
            # pending = Pending_Order.objects.filter(Q(user_icontains= query) | Q(orderId_icontains=query)).order_by("created_at", "DESC")
             
        return render(request, "admin/pending_orders.html", {"pending_orders": pending})
    else:
        return redirect("home")
    
def confirm_order(request, orderId):
    if request.user.is_authenticated and request.user.is_superuser:
        user_order = Pending_Order.objects.get(orderId=orderId)
        user = user_order.user
        order_items = user_order.pending_order_item.all()
        confirmed_order = Confirmed_Order.objects.create(user=user, orderId=orderId, total_cost=user_order.total_cost)
        
        #get all pending order items
        for item in order_items:
            Confirmed_order_items.objects.create(order=confirmed_order, item_name=item.item_name, item_quantity=item.item_quantity,
                                                 item_price=item.item_price, item_total_cost=item.item_total_cost)
            
        user_order.delete()
        
        return pending_orders(request)
    
def confirmed_orders(request):
    orders = Confirmed_Order.objects.all()
    
    return render(request, "admin/confirmed_orders.html", {"orders": orders})
        
        
        
        
        
    
            
                
            
        
        
            
        
    
            
            
            
        
        

        
    
                
        
    

    
            
        
        
        
        
    
    
    
