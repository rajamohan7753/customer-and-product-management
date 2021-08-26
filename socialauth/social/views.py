from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.models import User
from .forms import LoginForm,UserRegistrationForm, OrderForm
from .models import Customer,Product,Order,Tag
from django.forms import inlineformset_factory
from .filters import OrderFilter
from django.contrib.auth.decorators import login_required
#from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
# Create your views here.

def products(request):
    products=Product.objects.all()
    return render(request,'products.html',{'products':products})

def customers(request,pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    order_count = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs
    context = {'customer':customer,'orders':orders,'order_count':order_count,'myFilter':myFilter}
    return render(request,'customers.html',context)


@login_required(login_url='login')
def dashboard(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_customers = customers.all()

    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='pending').count()
    context = {'orders':orders,'customers':customers,'total_customers':total_customers,
    'total_orders':total_orders,'delivered':delivered,'pending':pending}
    return render(request,'dashboard.html',context)

def create_Order(request,pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product','status'))
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(instance=customer)
    #form = OrderForm(initial={'customer':customer})
    if request.method == 'POST':
        #form=OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = {'formset':formset}
    return render(request,'order_form.html',context)

def Update_Order(request,pk):

    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form=OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form':form,'order':order}
    return render(request,'order_form.html',context)


def delete_Order(request,pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')
    context = {'item':order}

    return render(request,'delete.html', context)

def login(request):
    if request.method =='POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,Username=cd['username'],Password=['password'])
            if user is None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated Sucessfully')
                else:
                    return HttpResponse("Disabled account")
            else:
                return HttpResponse("Invalid Login")
    else:
        form=LoginForm()
    return render(request,'registration/login.html',{'form':form})

def logout_view(request):
    logout(request)
    #return redirect('login')
    return render(request,'registration/logout.html')


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request,'register_done.html',{'new_user':new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,'registration/register.html',{'user_form':user_form})
