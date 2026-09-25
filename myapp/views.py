from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum

# Create your views here.
def index_view(request):
    
    if not request.user.is_authenticated:
        return redirect('login_page')
    
    product=products.objects.all()           #to show all products in index page
    
    context={
        'productdata':product,
    }
    
    return render(request,'pages/index.html',context)

def about_view(request):
    return render(request,'pages/about.html')

def login_view(request):
    
    if request.method=='POST':
        print("Working in this view")
        username=request.POST.get('username')
        password=request.POST.get('password')
        
        if not username or not password:
            messages.error(request,'please fill in all fields.')
            return redirect('login_page')
            
        user=User.objects.filter(username=username).first()
        
        if user is not None and user.check_password(password):
            login(request,user)
            messages.success(request,'Login Successful')
            return redirect('index_page')
        else:
            messages.error(request,'invalid username or password')
            return redirect('login_page')
    
    return render(request,'pages/login.html')

def register_view(request):
    if request.method == 'POST':
        #process the form data
        user_name=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        
        
        
        if not user_name or not email or not password:
            messages.error(request,'Please fill in all fields.')
            return redirect('register_page')
        
        if User.objects.filter(username=email).exists():
            messages.error(request,'Username already exist.')
            return redirect('register_page')
        
        user_data = User.objects.create_user(
    username=email,
    first_name=user_name,
    email=email,
    password=password
)
        
        user_data.save()
        messages.success(request,'Registration successful. please login!')
        return redirect('login_page')
        
        
    return render(request,'pages/register.html')

def logout_view(request):
    
    print("Logout view called")
    logout(request)
    messages.success(request,'You have been logged out successfully')
    return redirect('login_page')

def forget_view(request):
    
    if request.method=='POST':
        
        username=request.POST.get('username')
        password=request.POST.get('password')
        cpassword=request.POST.get('cpassword')
        
        print(username)
        print(password)
        print(cpassword)
        
        if not username or not password or not cpassword:
            messages.error(request,'Please fill all fields')
            return redirect('forget_page')
        
        if password != cpassword:
            messages.error(request,'Password does not match')
            return redirect('forget_page')
        
        user_is=User.objects.filter(username=username).first()
        
        if user_is is not None:
            user_is.set_password(password)
            user_is.save()
            messages.success(request,'Password reset successfully.Please login with your new password')
            return redirect('login_page')
        
    return render(request,'pages/forget.html')

def add_to_cart_view(request,product_id):
    
    if not request.user.is_authenticated:
        messages.error(request,"You need to be logged in to add items to the cart")
        return redirect('login_page')
    
    productis=products.objects.filter(id=product_id).first()
    
    if productis is None:
        messages.error(request,'Product not found')
        return redirect('index_page')
    
    user_cart, created=UserCart.objects.get_or_create(user=request.user)
    
    cart_item, created=CartItems.objects.get_or_create(cart=user_cart,product=productis)
    
    if not created:
        cart_item.quantity+=1
        cart_item.save()
        
    messages.success(request,f'Added {productis.name} to your cart.')
    return redirect('index_page')


def cart_count(request):
    if not request.user.is_authenticated:
        messages.error(request,'You need to be logged in to view your cart')
        return redirect('login_page')
    
    user_cart,created=UserCart.objects.get_or_create(user=request.user)
    
    cart_count=user_cart.cart_items.count()
    
    return JsonResponse({
        'status': True,
        'cart_count': cart_count
    })
   
def cart_items(request):
    if not request.user.is_authenticated:
        messages.error(request,'you need to first login')
        return redirect('login_page')
    
    user_cart,created=UserCart.objects.get_or_create(user=request.user)
    cart_items=user_cart.cart_items.all()
    
    total_items = sum(item.quantity for item in cart_items)
    subtotal = sum(item.product.price * item.quantity for item in cart_items)

    context = {
        'cart_items': cart_items,
        'total_items': total_items,
        'subtotal': subtotal,
        'total_amount': subtotal,
    }
    
    return render(request,'pages/cartItems.html',context) 

def view_details(request, product_id):
    product = get_object_or_404(products, id=product_id)

    context = {
        'product': product,
    }
    return render(request, 'pages/viewDetails.html', context) 


def update_cart(request, id, action):

    if not request.user.is_authenticated:
        messages.error(request,'You need to be logged in to update your cart.')
        return redirect("login_page")

    cart_item = CartItems.objects.filter(id=id,cart__user=request.user).first()

    if cart_item is None:
        messages.error(request,'Cart item not found')
        return redirect('cart_items')

    if action == 'increase':
        cart_item.quantity += 1

    elif action == 'decrease':
        cart_item.quantity -= 1

        if cart_item.quantity <= 0:
            cart_item.delete()
            messages.success(request,'Item removed from cart.')
            return redirect('cart_items')

    cart_item.save()
    return redirect('cart_items')