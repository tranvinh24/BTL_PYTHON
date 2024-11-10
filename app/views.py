from django.shortcuts import redirect, render
from django.http import HttpResponse,JsonResponse
from .models import *
import json
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
# Create your views here.
def register(request):
    form = CreateUserForm()
    
    if request.method=="POST":
        form= CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    categories = Category.objects.filter(is_sub=False)
    context={'form':form,'categories':categories}
    return render(request,'app/register.html',context)
def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method=="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:messages.info(request,'user or password not correct!')
    categories = Category.objects.filter(is_sub=False)        
    context={'categories':categories}
    return render(request,'app/login.html',context)
def logoutPage(request):
    logout(request)
    return redirect('login')
def home(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer,complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items=[]
        order = {'get_cart_items':0,'get_cart_total':0}
        cartItems = order['get_cart_items']
    categories = Category.objects.filter(is_sub=False)
    products = Product.objects.all()
    context={'categories':categories,'products': products,'cartItems':cartItems}
    return render(request,'app/home.html',context)
def cart(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer,complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items=[]
        order = {'get_cart_items':0,'get_cart_total':0}
        cartItems = order['get_cart_items']
    categories = Category.objects.filter(is_sub=False)
    context={'items':items,'order':order,'cartItems':cartItems,'categories':categories}
    return render(request,'app/cart.html',context)
def checkout(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer,complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items   
    else:
        items=[]
        order = {'get_cart_items':0,'get_cart_total':0}
        cartItems = order['get_cart_items']
    categories = Category.objects.filter(is_sub=False)
    context={'items':items,'order':order,'cartItems':cartItems,'categories':categories}
    if request.method == 'POST':
        messages.success(request, "Đặt hàng thành công!")
        return redirect('checkout')  # Hoặc tới trang khác nếu muốn
    return render(request,'app/checkout.html',context)
def updateItem(request):
    data= json.loads(request.body)
    productId = data['productId']
    action = data['action']
    customer = request.user
    product = Product.objects.get(id = productId)
    order, created = Order.objects.get_or_create(customer = customer,complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order = order,product = product)
    if action == 'add':
        orderItem.quantity +=1
    elif action =='remove':
        orderItem.quantity -=1
    orderItem.save()
    if orderItem.quantity<=0:
        orderItem.delete()
    return JsonResponse('added',safe=False)
def search(request):
    if request.method=="POST":
        searched = request.POST["searched"]
        keys = Product.objects.filter(name__contains = searched)
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer,complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items=[]
        order = {'get_cart_items':0,'get_cart_total':0}
        cartItems = order['get_cart_items']
    products = Product.objects.all()
    categories = Category.objects.filter(is_sub=False)
    context={'products': products,'cartItems':cartItems}
    return render(request,'app/search.html',{"searched":searched,"keys":keys,'products': products,'cartItems':cartItems,'categories':categories})
def category(request):
    categories = Category.objects.filter(is_sub=False)
    active_category =  request.GET.get('category','')
    if active_category:
        products =  Product.objects.filter(category__slug= active_category)
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer,complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items=[]
        order = {'get_cart_items':0,'get_cart_total':0}
        cartItems = order['get_cart_items']
    products = Product.objects.all()
    context =  {'categories': categories,'products':products,'cartItems':cartItems,'active_category':active_category}
    return render(request,'app/category.html',context)
def detail(request):
    id = request.GET.get('id','')
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer,complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items=[]
        order = {'get_cart_items':0,'get_cart_total':0}
        cartItems = order['get_cart_items']    
    products =  Product.objects.filter(id=id)
    categories = Category.objects.filter(is_sub=False)
    context={'items':items,'order':order,'cartItems':cartItems,'categories':categories,'products':products}
    return render(request,'app/detail.html',context)