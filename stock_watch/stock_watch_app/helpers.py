'''
 # @ Author: Marco Duvacher
 # @ Create Time: 2022-11-10 00:13:47
 # @ Modified by: Marco Duvacher
 # @ Modified time: 2022-11-10 09:56:44
 # @ Description: Some fonctions used in the views. File created to make the code more readable.
 '''
#region -------------------- IMPORT -----------------------------------
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect, HttpRequest
from django.contrib import messages
import psycopg2
from datetime import date
from datetime import datetime
from datetime import timedelta
from .models import Product
#endregion -------------------- IMPORT --------------------------------

def get_product_from_request(request):
    """ Get the list of product objects ordered by the attribute given in the request

    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_
    """
    print(type(request))
    order_by = request.GET.get('order_by', 'date')
    all_product = Product.objects.all().order_by(order_by)
    return all_product

def get_gtin_from_request(request) -> int:
    '''
    Check if the gtin given is correct and return it or None if it's wrong
    '''
    try:
        gtin_to_test =  int(request.POST.get('gtin'))
    except ValueError:
        gtin_to_test = None
        messages.error(request, "This GTIN is not a number")
    return gtin_to_test

def get_date_from_request(request) -> tuple[bool, str]:
    '''
    Check if the date given is correct and return it or None if it's wrong
    '''
    date = request.POST.get('date')
    # Check the date format
    try:
        datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        messages.error(request, "Wrong date format, should be YYYY-MM-DD")
        date = None
    return date

def create_new_product_in_base(request: HttpRequest, new_gtin: int, new_date: datetime.date):
    """_summary_

    Args:
        request (HttpRequest): request that asked to create a new product
        new_gtin (int): gtin of the new product
        new_date (datetime.date): date of the new product
    """
    new_product = Product(gtin = new_gtin, date = new_date)
    try:
        new_product.save()
    except Exception as e:
        messages.error(request, f"Failed to created in base, error: {e}")
    messages.success(request, "GTIN created sucessfully")

def update_product_in_base(request: HttpRequest, product_to_update: Product, new_date: datetime.date):
    """Update the date of a product in Base

    Args:
        request (HttpRequest): the request of the update
        product_to_update (Product): the product to update
        new_date (datetime.date): the new date of the product
    """
    product_to_update.date = new_date
    try:
        product_to_update.save()
    except Exception as e:
        messages.error(request, f"Failed to update in base, error: {e}")
    messages.success(request, "GTIN updated sucessfully")