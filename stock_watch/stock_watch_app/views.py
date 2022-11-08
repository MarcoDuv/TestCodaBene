from django.shortcuts import render
from django.http import HttpResponse

def list_products(request):
    return render(request, 'stock_watch_app/products_list.html')
