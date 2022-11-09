from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect, HttpRequest
from django.contrib import messages
import psycopg2
import datetime
from .models import Product


def list_products(request):
    order_by = request.GET.get('order_by', 'date')
    all_product = Product.objects.all().order_by(order_by)
    all_gtin = {'product_list': all_product}
    return render(request, 'stock_watch_app/products_list.html', context=all_gtin)

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
        datetime.datetime.strptime(date, '%Y-%m-%d')
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
    return redirect('/stock_watch_app/list/')

def srch_gtin(request:HttpRequest):
    ''' The view that gets the gtin asked by user '''

    gtin_asked = request.POST['gtinasked']
    
    # Check if the gtin is valid
    try:
        gtin_asked = int(request.POST['gtinasked']) #TODO Sort by date
    except ValueError:
        if gtin_asked == '':    # If it's empty we display all the products (ie: delete filter)
            return redirect('/stock_watch_app/list/')
        else:
            messages.error(request, "GTIN must be a number")
            context = None

    # If it's valid, check if it's in the BDD
    else: 
        list_product = Product.objects.filter(gtin = gtin_asked)
        if list_product:
            context = {'product_list': list_product}
        else: 
            messages.error(request, "This GTIN is not registered")
            context = None

    return render(request, 'stock_watch_app/products_srch.html', context=context)

def logo_link(request):
    return redirect('/stock_watch_app/list/')