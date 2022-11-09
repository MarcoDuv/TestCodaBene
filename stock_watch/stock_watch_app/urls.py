from django.urls import path
from . import views

APP_NAME = 'StockWatch'

urlpatterns = [
    path('list/', views.list_products, name="list"),
    path('insertgtin/', views.insert_gtin, name="insertgtin"),
    path('srchgtin/', views.srch_gtin, name="srchgtin")
]