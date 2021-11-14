from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from .models import *
from .forms import *
from .filters import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import *
from django.contrib.auth.models import Group


# Create your views here.
def RegisterView(request):
    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()

            return redirect('accounts:login')

    context={'form':form}
    return render(request, 'accounts/register.html', context)

@unauthenticated_user
def LoginView(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request,'username or password not correct')
    return render(request, 'accounts/login.html')

def LogoutView(request):
    logout(request)
    return redirect('accounts:login')

@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['admin'])
def home(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()

    total_customers = customers.count()
    total_orders = orders.count()

    pending_orders = orders.filter(status='Pending').count()
    delivered_orders = orders.filter(status='Delivered').count()

    context={'customers':customers, 'orders':orders, 'total_customers':total_customers,
    'total_orders':total_orders, 'pending_orders':pending_orders, 'delivered_orders':delivered_orders}
    return render(request, 'accounts/dashboard.html', context)

@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['customer'])
def user_page(request):
    orders = request.user.customer.order_set.all()

    total_orders = orders.count()

    pending_orders = orders.filter(status='Pending').count()
    delivered_orders = orders.filter(status='Delivered').count()

    context = {'orders':orders, 'total_orders':total_orders,
    'pending_orders':pending_orders, 'delivered_orders':delivered_orders}
    return render(request, 'accounts/user.html', context)

@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['customer'])
def account_settings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)

        if form.is_valid():
            form.save()

    context={'form':form}
    return render(request, 'accounts/account_settings.html', context)

@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    products = Product.objects.all()

    context={'products':products}
    return render(request, 'accounts/products.html', context)

@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk):
    customer = Customer.objects.get(id=pk)

    orders = customer.order_set.all()
    total_orders = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context={'customer':customer, 'orders':orders, 'total_orders':total_orders, 'myFilter':myFilter}
    return render(request, 'accounts/customer.html', context)

@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['admin'])
def create_order(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=5)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(instance=customer, queryset=Order.objects.none())
    #form = OrderForm(initial={'customer': customer})

    if request.method == "POST":
        #form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customer)

        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = {'form':formset, 'customer':customer}
    return render(request, 'accounts/order_form.html', context)

@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['admin'])
def update_order(request, pk):
    order = Order.objects.get(id=pk)
    customer = Customer.objects.get(order=order)

    form = OrderForm(instance=order)

    if request.method == "POST":
        form = OrderForm(request.POST, instance=order)

        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form':form, 'customer':customer}
    return render(request, 'accounts/order_form.html', context)

@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['admin'])
def delete_order(request, pk):
    order = Order.objects.get(id=pk)

    if request.method =='POST':
        order.delete()
        return redirect('/')

    context = {'order':order}
    return render(request, 'accounts/delete_order.html', context)


@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['admin'])
def create_product(request):
    form = ProductForm()

    if request.method == "POST":
        form = ProductForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form':form}
    return render(request, 'accounts/product_form.html', context)


@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['admin'])
def update_product(request, pk):
    product = Product.objects.get(id=pk)
    form = ProductForm(instance=product)

    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)

        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form':form}
    return render(request, 'accounts/product_form.html', context)


@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['admin'])
def delete_product(request, pk):
    product = Product.objects.get(id=pk)

    if request.method =='POST':
        product.delete()
        return redirect('/')

    context = {'product':product}
    return render(request, 'accounts/delete_product.html', context)

