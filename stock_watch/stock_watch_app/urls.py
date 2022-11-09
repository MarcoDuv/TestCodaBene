from django.urls import path
from . import views

APP_NAME = 'StockWatch'

urlpatterns = [
    path('list/', views.list_products, name="list"),
    path('insertgtin/', views.insert_gtin, name="insertgtin"),
    path('list/query', views.srch_gtin, name="srchgtin"),#TODO add dynamic URL to the search (srchgtin/<int: gtin>/ for ex)
    path('list/home_link/', views.home_link, name='homelink')
]