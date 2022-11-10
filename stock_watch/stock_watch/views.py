'''
 # @ Author: Marco Duvacher
 # @ Create Time: 2022-11-10 10:09:46
 # @ Modified by: Marco Duvacher
 # @ Modified time: 2022-11-10 10:10:03
 # @ Description: Views for the project. Since we have only one app, this file contains only the
 view that allows us to be redirected to the app home page when we launch the server.
 '''

#region -------------------- IMPORTS -----------------------------------
from django.http import HttpResponseRedirect
from django.http import HttpRequest
#endregion -------------------------------------------------------------

def index(request: HttpRequest ) -> HttpResponseRedirect:
    """Redirect user to the StockWatch app main page

    Args:
        request (HttpRequest ): contains data about the request

    Returns:
        HttpResponseRedirect: Response that moves the given URL into a new one
    """
    return HttpResponseRedirect("/StockWatch/")
