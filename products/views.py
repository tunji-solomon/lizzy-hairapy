from django.shortcuts import render, redirect
from .models import Products, Category
from cloudinary.uploader import upload

# Create your views here.
def home(request):
    all_product = Products.objects.all()
    categories = Category.objects.all()
    if request.method =="POST":
        search = request.POST.get("search")
        if search:
            all_product = Products.objects.filter(name__icontains=search)
        price_by = request.POST.get("price")
        price = request.POST.get("price-field")
        category = request.POST.get("category")
        if price_by:
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
            all_product = Products.objects.filter(category__title = category)
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

def search_product(request):
    pass
    

    
            
        
        
        
        
    
    
    
