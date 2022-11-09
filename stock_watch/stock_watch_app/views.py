from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect, HttpRequest
from django.contrib import messages
import psycopg2
from datetime import date
from datetime import datetime
from datetime import timedelta
from .models import Product

TRESHOLD_DAYS_DANGER = date.today() + timedelta(days=1)
TRESHOLD_DAYS_WARNING = date.today() + timedelta(days=3)

def list_products(request):
    order_by = request.GET.get('order_by', 'date')
    all_product = Product.objects.all().order_by(order_by)
    context = {'product_list': all_product, 'time_danger': TRESHOLD_DAYS_DANGER, 'time_warning':TRESHOLD_DAYS_WARNING, 'today': date.today()}
    return render(request, 'products_list.html', context=context)

def insert_gtin(request:HttpRequest):
    ''' View to insert a new gtin by user '''
    date = request.POST['date']
    # Check if the gtin is a number
    try:
        new_gtin =  int(request.POST['gtin'])
    except ValueError:
        new_gtin = None
        messages.error(request, "This GTIN is not a number")

    #TODO Check if it fits the shape of a gtin

    # Check the date format
    try:
        datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        messages.error(request, "Wrong date format, should be YYYY-MM-DD")
        date = None

    if (new_gtin is not None) & (date is not None):
        try:
            existing_product = Product.objects.get(gtin = new_gtin)
        except Product.DoesNotExist:
            new_product = Product(gtin = new_gtin, date = request.POST['date'])
            new_product.save()
            messages.success(request, "GTIN created sucessfully")
        else:
            existing_product.date = date
            existing_product.save()
            messages.success(request, "GTIN updated sucessfully")
    return redirect('/StockWatch/')

def srch_gtin(request:HttpRequest):
    ''' The view that gets the gtin asked by user '''
    
    query = request.POST.get('gtinasked')

    # Check if the gtin is valid
    try:
        gtin_asked = int(request.POST.get('gtinasked'))
    except TypeError:
        if query is None: # If it's none we go back to the list display
            return redirect('/StockWatch/')
        else:
            messages.error(request, "Type Error for GTIN")
            return redirect('/StockWatch/')
    except ValueError:
        if query == '':    # If it's empty we display all the products (ie: delete filter)
            return redirect('/StockWatch/')
        else:
            messages.error(request, "GTIN must be a number")
            return redirect('/StockWatch/')

    # If it's valid, check if it's in the BDD
    else: 
        list_product = Product.objects.filter(gtin = gtin_asked)
        if list_product:
            context = {'product_list': list_product}
        else: 
            messages.warning(request, "This GTIN is not registered")
            return redirect('/StockWatch/')

    return render(request, 'products_list.html', context=context)

def home_link(request):
    return redirect('/StockWatch/')

def error_404_view(request, exception):
   
    # we add the path to the the 404.html file
    # here. The name of our HTML file is 404.html
    return render(request, '404.html')

def tag(a,b):
    return a+b