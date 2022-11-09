from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect, HttpRequest
from .models import Product

def list_products(request):
    return render(request, 'stock_watch_app/products_list.html')

def insert_gtin(request:HttpRequest):
    ''' View to insert a new gtin by user '''
    date = request.POST['date']
    # Check if the gtin is a number
    try:
        new_gtin =  int(request.POST['gtin'])
    except:
        new_gtin = None

    #TODO Check if it fit the shape of a gtin

    if (new_gtin is not None) & (date is not None):
        product = Product(gtin = new_gtin, date = request.POST['date'])
        product.save()
    return redirect('/stock_watch_app/list/')

def srch_gtin(request:HttpRequest):
    ''' The view that gets the gtin asked by user '''
    gtin_asked = request.POST['gtinasked']
    # Check if the gtin is a number
    try:
        gtin_asked = int(request.POST['gtinasked'])
    except:
        gtin_asked = None

    # Check if the gtin exists
    if gtin_asked is not None:
        gtin_asked = {'product_list': Product.objects.filter(gtin = gtin_asked)}
    return render(request, 'stock_watch_app/products_list.html', context=gtin_asked)