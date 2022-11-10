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

def is_valid_gtin(gtin_to_test) -> tuple[bool, str]:
    '''
    Check if the gtin given in input has a correct type
    '''
    try:
        int(gtin_to_test)
    except TypeError:
        if gtin_to_test is None: # If it's none we go back to the list display
            return 0
        else:
            err_msg = "Type Error for GTIN"
            return 0, err_msg
    except ValueError:
        if gtin_to_test == '':    # If it's empty we display all the products (ie: delete filter)
            return 0
        else:
            err_msg = "GTIN must be a number"
            return 0, err_msg
    else:
        return 1, None