from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect, HttpRequest
from .models import Product

def list_products(request):
    return render(request, 'stock_watch_app/products_list.html')

def insert_gtin(request:HttpRequest):
    product = Product(gtin = request.POST['gtin'], date = request.POST['date'])
    product.save()
    return redirect('/stock_watch_app/list/')