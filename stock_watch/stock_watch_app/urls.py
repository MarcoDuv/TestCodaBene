from django.urls import path
from . import views

APP_NAME = 'StockWatch'

urlpatterns = [
    path('list/', views.list_products)
]