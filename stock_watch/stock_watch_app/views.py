from django.shortcuts import render
from django.http import HttpResponse

def list_products(request):
    return HttpResponse("from list_prodcuts")
