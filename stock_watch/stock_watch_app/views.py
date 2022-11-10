'''
 # @ Author: Marco Duvacher
 # @ Create Time: 2022-11-08 15:45:42
 # @ Modified by: Marco Duvacher
 # @ Modified time: 2022-11-10 10:02:43
 # @ Description: Contain all the views usefull for the application
 (ie: Python functions or classes that receive a web request and return a web response)
 '''

#region -------------------- IMPORTS -----------------------------------
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect, HttpRequest
from django.contrib import messages
from typing import Union
from datetime import date
from datetime import datetime
from datetime import timedelta
from .models import Product
from .helpers import get_product_from_request
from .helpers import get_gtin_from_request
from .helpers import get_date_from_request
from .helpers import create_new_product_in_base
from .helpers import update_product_in_base
#endregion -------------------------------------------------------------

TRESHOLD_DAYS_DANGER = date.today() + timedelta(days=1)
TRESHOLD_DAYS_WARNING = date.today() + timedelta(days=3)

def home(request: HttpRequest) -> HttpResponse:
    """Views called on a request on the main page of the app.

    It takes in DB the list of all products and add it in the context of the response returned.
    It puts also in the response some datetime.date constants
    used to know if the product expiring date is close enoug.

    Args:
        request (HttpRequest): contains data about the request (optional content: order_by )

    Returns:
        HttpResponse: The Http response containing the related html and context
        (contains -> product_list: QuerySet[Product], time_danger, time_warning, today: DateTime.date)
    """
    all_product = get_product_from_request(request)
    context = { 'product_list': all_product,
                'time_danger': TRESHOLD_DAYS_DANGER,
                'time_warning':TRESHOLD_DAYS_WARNING,
                'today': date.today()}
    return render(request, 'home.html', context=context)

def insert_gtin(request:HttpRequest) -> HttpResponseRedirect:
    """Views called  when there is a request of user trying to insert a new product.

    It checks the Gtin and date format, then check if it is already in DB.
    If yes: Update the date of the corresponding GTIN
    If no: Create a new product.

    Args:
        request (HttpRequest): contains data about the request (requires: date & gtin)

    Returns:
        HttpResponseRedirect: Redirect to another URL (here the main page of the app)
    """

    new_gtin = get_gtin_from_request(request)
    new_date = get_date_from_request(request)

    if (new_gtin is not None) & (new_date is not None):
        try:
            existing_product = Product.objects.get(gtin = new_gtin)
        except Product.DoesNotExist:
            create_new_product_in_base(request, new_gtin, new_date)
        else:
            update_product_in_base(request, existing_product, new_date)
    return redirect('/StockWatch/')

def srch_gtin(request:HttpRequest) -> Union[HttpResponseRedirect, HttpRequest]:
    """ View called on a request of input user in the GTIN search field. 

    It checks if the gtin is correct, then if it is in DB and return the adapated response. 

    Args:
        request (HttpRequest): contains data about the request (requires: date & gtin)

    Returns:
         Union[HttpResponseRedirect, HttpRequest]: 
         Either a response that redirects to the home page (if wrong gtin asked) or
         a response that renders to the URL which display the filtered gtin (if right one)
    """
    
    query = request.POST.get('gtinasked')

    # Check if the gtin is valid
    try:
        gtin_asked = int(query)
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

    return render(request, 'home.html', context=context)

def home_link(request):
    """View called on a request raised when user click on a link that redirect to the main page

    Args:
        request (HttpRequest): The request raised on a home page link click

    Returns:
        HttpResponseRedirect: Change the current URL to the main page app one
    """
    return redirect('/StockWatch/')

def error_404_view(request, exception):
    """View called on a 404 error request

    Args:
        request (HttpRequest): contains data of the request
        exception (Exception): (unused here)

    Returns:
        HttpResponse: http response to display the 404.html page
    """
    return render(request, '404.html')